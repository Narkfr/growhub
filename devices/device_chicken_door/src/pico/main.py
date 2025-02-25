import secrets
import time

import machine
import network
import umqtt.simple as mqtt

# Wi-Fi Configuration
SSID = secrets.SSID
PASSWORD = secrets.PASSWORD
MOSQUITTO = secrets.MOSQUITTO

# MQTT Configuration
BROKER = MOSQUITTO
TOPIC = 'growhub/chicken/door'

# Setup LED
openLed = machine.Pin(15, machine.Pin.OUT)
closeLed = machine.Pin(16, machine.Pin.OUT)
wifiLed = machine.Pin(17, machine.Pin.OUT)

# Setup Moteur (L298N)
IN1 = machine.Pin(3, machine.Pin.OUT)  # Direction 1
IN2 = machine.Pin(4, machine.Pin.OUT)  # Direction 2
enable_pin = machine.PWM(machine.Pin(2))  # Activation moteur (PWM)
enable_pin.freq(1000)  # Fréquence PWM
end_open = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)  # Capteur d'ouverture
end_close = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)

def set_motor_speed(duty_cycle):
    """Définit la vitesse du moteur (0-1023)."""
    enable_pin.duty_u16(duty_cycle)

def rotate_motor(direction, led_status, speed=15000):
    """Fait tourner le moteur dans la direction donnée avec la vitesse spécifiée et clignote la LED."""
    
    # Initialisation de la vitesse du moteur
    set_motor_speed(speed)
    
    # Contrôle de la direction du moteur
    if direction == "open":
        IN1.on()
        IN2.off()
    elif direction == "close":
        IN1.off()
        IN2.on()

    # Affichage des états des capteurs
    print("Ouverture:", end_open.value())
    print("Fermeture:", end_close.value())

    # Clignotement de la LED pendant le mouvement
    led_status.on()
    time.sleep(0.5)
    led_status.off()
    time.sleep(0.5)

    # Attente de la fin de course en fonction de la direction
    while True:
        if direction == "open" and end_open.value() == 0:
            print("Fin de course ouverture atteinte.")
            stop_motor(led_status)
            break  # Arrêt du moteur si capteur ouvert détecté
        elif direction == "close" and end_close.value() == 0:
            print("Fin de course fermeture atteinte.")
            stop_motor(led_status)
            break  # Arrêt du moteur si capteur fermé détecté
        time.sleep(0.1)  # Vérification toutes les 100ms

def stop_motor(led_status):
    """Arrête le moteur et allume la LED."""
    IN1.off()
    IN2.off()
    led_status.on()

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to Wi-Fi...")

    while not wlan.isconnected():
        wifiLed.on()
        time.sleep(0.5)
        wifiLed.off()
        time.sleep(0.5)

    wifiLed.on()
    print("Connected to Wi-Fi:", wlan.ifconfig())

def on_message(topic, msg):
    print("Received message:", msg)
    if msg == b"open":
        rotate_motor("open", openLed, speed=30000)  # Vitesse élevée
        closeLed.off()
    elif msg == b"close":
        rotate_motor("close", closeLed, speed=30000)
        openLed.off()

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
