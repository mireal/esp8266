import network
from umqtt.simple import MQTTClient
import machine
import time
import ubinascii
import dht
from config import WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_TOPIC


# Pin connected to DHT22 sensor
dht_pin = machine.Pin(2)

# Create a DHT22 object
d = dht.DHT22(dht_pin)

# Function to read temperature and humidity from DHT22 sensor
def read_dht22():
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    return temp, hum

# Define function to connect to WiFi network
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('WiFi connected!')
    print('Network config.py:', sta_if.ifconfig())

# Define function to connect to MQTT broker
def connect_mqtt():
    client_id = ubinascii.hexlify(machine.unique_id()).decode()
    client = MQTTClient(client_id, MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)
    client.connect()
    print('MQTT connected!')
    return client

# Connect to WiFi network
connect_wifi()

# Connect to MQTT broker
mqtt = connect_mqtt()

# Send random number to MQTT broker every 5 seconds
while True:
    try:
        temp, hum = read_dht22()
        value = f'temperature: {temp}C, humidity: {hum}%'
    except OSError as e:
        value = f'Failed to read data from DHT22 sensor: {e}'
    mqtt.publish(MQTT_TOPIC, value)
    print('Published:', value)
    time.sleep(5)
    machine.idle()