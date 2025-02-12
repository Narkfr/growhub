import network
import umqtt.simple as mqtt
import machine
import secrets
import time

# Wi-Fi Configuration
SSID = secrets.SSID
PASSWORD = secrets.PASSWORD
MOSQUITTO = secrets.MOSQUITTO

# MQTT Configuration
BROKER = MOSQUITTO
TOPIC = 'growhub/chicken/door'

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print(wlan.isconnected())

    while not wlan.isconnected():
        pass

    print("Connected to Wi-Fi:", wlan.ifconfig())

# Callback for MQTT messages
def on_message(topic, msg):
    print("Received message:", msg)
    if msg == b"open":
        greenLed.on()
        redLed.off()
    elif msg == b"close":
        greenLed.off()
        redLed.on()

# Setup LED
redLed = machine.Pin(15, machine.Pin.OUT)
greenLed = machine.Pin(16, machine.Pin.OUT)

# Connect to Wi-Fi
connect_wifi()

def connect_mqtt():
    client = mqtt.MQTTClient("pico_client", BROKER)
    client.set_callback(on_message)
    
    try:
        client.connect()
        print("Connected to MQTT broker")
    except OSError as e:
        print("Connection failed:", e)
        return None
    return client

# Essayer de se connecter au serveur MQTT
client = connect_mqtt()
if client:
    client.subscribe(TOPIC)
    print("Subscribed to topic:", TOPIC)
else:
    print("MQTT connection failed")

# Boucle principale pour recevoir les messages
while True:
    if client:
        client.check_msg()  # Vérifie les nouveaux messages
    time.sleep(1)  # Donne du temps à l'ESP pour gérer la connexion