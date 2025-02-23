import threading
from datetime import datetime

import paho.mqtt.client as mqtt
import redis
from celery import Celery
from config import env, routes
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Celery Configuration
app.config["CELERY_BROKER_URL"] = f"redis://{env.REDIS_HOST}:{env.REDIS_PORT}/0"
app.config["CELERY_RESULT_BACKEND"] = f"redis://{env.REDIS_HOST}:{env.REDIS_PORT}/0"
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

@celery.task
def mqtt_publish(topic, message):
    print(f"📢 Publishing to topic: {topic}, message: {message}")
    mqtt_client.publish(f"{env.MQTT_TOPIC}/{topic}", message)
    print("✅ Message sent")

# MQTT Configuration
MQTT_BROKER = env.MQTT_BROKER
MQTT_PORT = env.MQTT_PORT
MQTT_TOPIC = env.MQTT_TOPIC

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("✅ MQTT client connected")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Message receivef on {msg.topic}: {msg.payload.decode()}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
mqtt_thread.daemon = True
mqtt_thread.start()

def schedule_mqtt(topic, message, delay=0, scheduled_time=None):
    if scheduled_time:
        try:
            execution_time = datetime.strptime(scheduled_time,"%Y-%m-%d %H:%M:%S")
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

# Redis Configuration
REDIS_HOST = env.REDIS_HOST
REDIS_PORT = env.REDIS_PORT
redisServer = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def connect_redis():
    try:
        redisServer.ping()
        print("✅ Connected to Redis successfully!")
    except redis.ConnectionError:
        print("❌ Failed to connect to Redis.")
        exit(1)

# Routes
@app.route(routes.MQTT, methods=["POST"])
def mqtt_post():
    try:
        if not mqtt_client.is_connected():
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

@app.route(routes.INDEX)
def index():
    return render_template('index.html', routes=routes)

@app.route(routes.CHICKEN)
def chicken():
    return render_template('chicken.html', routes=routes, door_status="open")

if __name__ == "__main__":
    connect_redis()
    app.run(debug=True, host="0.0.0.0")
