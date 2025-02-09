from flask import Flask, render_template, request, jsonify
from config import routes, env
import paho.mqtt.client as mqtt
import redis

app = Flask(__name__)

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
        print(f"Publishing to topic: {topic}, message: {message}")

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

if __name__ == '__main__':
    connect_mqtt()
    connect_redis()
    app.run(debug=True, host='0.0.0.0')