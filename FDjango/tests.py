from django.test import TestCase
import json
import paho.mqtt.client as mqtt

mqtt_broker_address = "test.mosquitto.org"
mqtt_broker_port = 1883

list_of_lights = ["0xd87a3bfffe0f2231", "0x5cc7c1fffe355388"]

# Topic for publishing commands to Zigbee2MQTT
mqtt_command_topic = f"zigbee2mqtt/{list_of_lights[1]}/set"  # Replace with your device's topic

# Payload to adjust brightness and turn on the lamp
brightness_increase_payload = {
    "brightness": 10,  # Adjust brightness value as needed
    "color": {"x": 0.2361, "y": 0.1404},
    "color_options": {"execute_if_off": True},
    "color_temp": 5,
    "state": "ON",
}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_command_topic)

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload}")

    # Connect to the MQTT broker

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker_address, mqtt_broker_port, 60)

# Publish the payload to adjust brightness and turn on the lamp
client.publish(mqtt_command_topic, json.dumps(brightness_increase_payload))

# Wait for a short time to allow the message to be sent
client.loop_start()
client.loop_stop()