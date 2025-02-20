from datetime import datetime

import paho.mqtt.client as mqtt
import redis
from celery import Celery
from config import env, routes
from flask import Flask, jsonify, request

app = Flask(__name__)

# Celery Configuration
app.config["CELERY_BROKER_URL"] = f"redis://{env.REDIS_HOST}:{env.REDIS_PORT}/0"
app.config["CELERY_RESULT_BACKEND"] = f"redis://{env.REDIS_HOST}:{env.REDIS_PORT}/0"
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

# MQTT Configuration
MQTT_BROKER = env.MQTT_BROKER
MQTT_PORT = env.MQTT_PORT
MQTT_TOPIC = env.MQTT_TOPIC

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Redis Configuration
REDIS_HOST = env.REDIS_HOST
REDIS_PORT = env.REDIS_PORT
redisServer = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def connect_mqtt():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()
        print("✅ MQTT client connected")
    except (mqtt.MQTTException, ConnectionRefusedError) as e:
        print(f"❌ Error connecting to MQTT broker: {e}")


def connect_redis():
    try:
        redisServer.ping()
        print("✅ Connected to Redis successfully!")
    except redis.ConnectionError:
        print("❌ Failed to connect to Redis.")
        exit(1)


@celery.task
def mqtt_publish(topic, message):
    print(f"📢 Publishing to topic: {topic}, message: {message}")
    local_client = mqtt.Client()
    local_client.connect(env.MQTT_BROKER, env.MQTT_PORT)
    local_client.publish(f"{env.MQTT_TOPIC}/{topic}", message)
    local_client.disconnect()
    print("✅ Message sent via new MQTT client")


def schedule_mqtt(topic, message, delay=0, scheduled_time=None):
    if scheduled_time:
        try:
            execution_time = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")
            delay = (execution_time - datetime.now()).total_seconds()
            if delay < 0:
                return {"error": "Scheduled time is in the past"}, 400
        except ValueError:
            return {"error": "Invalid datetime format"}, 400

    print(
        f"🕒 Scheduling message: {message} to topic: {topic} "
        f"{'at ' + scheduled_time if scheduled_time else 'in ' + str(delay) + ' seconds'}"
    )

    mqtt_publish.apply_async(args=[topic, message], countdown=delay)
    return {
        "status": "scheduled",
        "topic": topic,
        "message": message,
        "delay": delay,
        "scheduled_time": scheduled_time,
    }


@app.route(routes.MQTT, methods=["POST"])
def mqtt_post():
    try:
        if not client.is_connected():
            return jsonify({"error": "MQTT client is not connected"}), 500
        data = request.json
        return jsonify(
            schedule_mqtt(
                topic=data.get("topic"),
                message=data.get("message"),
                delay=data.get("delay"),
                scheduled_time=data.get("datetime"),
            )
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    connect_mqtt()
    connect_redis()
    app.run(debug=True, host="0.0.0.0")
