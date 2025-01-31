from flask import Flask, render_template, request, jsonify
from config import routes, env
import paho.mqtt.client as mqtt

app = Flask(__name__)

# MQTT Configuration
MQTT_BROKER = env.MQTT_BROKER  # Changez si le broker est sur une autre machine
MQTT_PORT = env.MQTT_PORT
MQTT_TOPIC = env.MQTT_TOPIC

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Connect to MQTT Broker
def connect_mqtt():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()
        print("MQTT client connected")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

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

if __name__ == '__main__':
    connect_mqtt()
    app.run(debug=True, host='0.0.0.0')