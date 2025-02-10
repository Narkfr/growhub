from datetime import datetime
from flask import Flask, render_template, request, jsonify
from config import routes, env
import paho.mqtt.client as mqtt
import redis
from celery import Celery

app = Flask(__name__)

# Celery Configuration
app.config['CELERY_BROKER_URL'] = f'redis://{env.REDIS_HOST}:{env.REDIS_PORT}/0'
app.config['CELERY_RESULT_BACKEND'] = f'redis://{env.REDIS_HOST}:{env.REDIS_PORT}/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# MQTT Configuration
MQTT_BROKER = env.MQTT_BROKER  # Changez si le broker est sur une autre machine
MQTT_PORT = env.MQTT_PORT
MQTT_TOPIC = env.MQTT_TOPIC

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Redis Configuration
REDIS_HOST = env.REDIS_HOST
REDIS_PORT = env.REDIS_PORT
redisServer = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Connect to MQTT Broker
def connect_mqtt():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()
        print("✅ MQTT client connected")
    except (mqtt.MQTTException, ConnectionRefusedError) as e:
        print(f"❌ Error connecting to MQTT broker: {e}")

# Connect to Redis
def connect_redis():
    try:
        redisServer.ping()
        print("✅ Connected to Redis successfully!")
    except redis.ConnectionError:
        print("❌ Failed to connect to Redis.")
        exit(1)

# Celery Task to publish to MQTT
@celery.task
def mqtt_publish(topic, message):
    print(f"📢 Publishing to topic: {topic}, message: {message}")

    local_client = mqtt.Client()
    local_client.connect(env.MQTT_BROKER, env.MQTT_PORT)
    local_client.publish(f'{env.MQTT_TOPIC}/{topic}', message)
    local_client.disconnect()

    print("✅ Message sent via new MQTT client")

@app.route(routes.INDEX)
def index():
    return render_template('index.html', routes=routes)

@app.route(routes.CHICKEN)
def chicken():
    return render_template('chicken.html', routes=routes, door_status="open")

@app.route(routes.MQTT, methods=['POST'])
def mqtt_post():
    try:
        if not client.is_connected():
            return jsonify({"error": "MQTT client is not connected"}), 500
        data = request.json
        topic = data.get("topic")
        message = data.get("message")
        print(f"📢 Publishing to topic: {topic}, message: {message}")

        # Publish to MQTT topic
        client.publish(f'{env.MQTT_TOPIC}/{topic}', message)
        return jsonify({"topic": topic, "message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route(routes.REDIS, methods=['POST'])
def redis_post():
    try:
        data = request.json
        print(data)
        key = data.get("key")
        value = data.get("value")
        print(f"Setting key: {key}, value: {value}")

        # Set key-value pair in Redis
        redisServer.set(key, value)
        return jsonify({"key": key, "value": value})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/schedule_tasks', methods=['POST'])
def schedule_tasks():
    data = request.json
    tasks = data.get("tasks")
    print(f"🕒 Received {len(tasks)} tasks")

    for task in tasks:
        topic = task.get("topic")
        message = task.get("message")
        delay = task.get("delay")
        print(f"🕒 Scheduling message: {message} to topic: {topic} in {delay} seconds")

        mqtt_publish.apply_async(args=[topic, message], countdown=delay)
    
    return jsonify({"status": "scheduled", "tasks": len(tasks)})

@app.route('/schedule/mqtt', methods=['POST'])
def schedule_mqtt():
    """ Schedule a MQTT message """
    data = request.json
    topic = data.get("topic")
    message = data.get("message")
    delay = data.get("delay", 120)  # Default delay: 2 minutes
    print(f"🕒 Scheduling message: {message} to topic: {topic} in {delay} seconds")

    mqtt_publish.apply_async(args=[topic, message], countdown=delay)
    return jsonify({"status": "scheduled", "topic": topic, "message": message, "delay": delay})

@app.route('/schedule/mqtt/datetime', methods=['POST'])
def schedule_mqtt_datetime():
    """ Schedule a MQTT message at a specific date/time """
    data = request.json
    topic = data.get("topic")
    message = data.get("message")
    scheduled_time = data.get("datetime")  # Format: 'YYYY-MM-DD HH:MM:SS'
    print(f"🕒 Scheduling message: {message} to topic: {topic} at {scheduled_time}")

    try:
        execution_time = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")
        delay = (execution_time - datetime.now()).total_seconds()
        if delay < 0:
            return jsonify({"error": "Scheduled time is in the past"}), 400

        mqtt_publish.apply_async(args=[topic, message], countdown=delay)
        return jsonify({
            "status": "scheduled", 
            "topic": topic, 
            "message": message, 
            "datetime": scheduled_time
        })
    except ValueError:
        return jsonify({"error": "Invalid datetime format"}), 400


if __name__ == '__main__':
    connect_mqtt()
    connect_redis()
    app.run(debug=True, host='0.0.0.0')
