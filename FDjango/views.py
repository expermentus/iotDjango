from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import json
import paho.mqtt.client as mqtt
import skimage.color
import numpy as np


def loadBase(request):
    return render(request, "FDjango/base.html")

def loadClock(request):
    return render(request, "FDjango/clock.html")

def clock_start(request):
    mqtt_broker_address = "test.mosquitto.org"
    mqtt_broker_port = 1883

    list_of_lights = ["0xd87a3bfffe0f2231", "0x5cc7c1fffe355388"]

    mqtt_command_topic = f"zigbee2mqtt/play"

    play_payload = {
        "play": "play",
    }

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(mqtt_command_topic)

    def on_message(client, userdata, msg):
        print(f"Received message on topic {msg.topic}: {msg.payload}")


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker_address, mqtt_broker_port, 60)

    # Publish the payload to adjust brightness and turn on the lamp
    client.publish(mqtt_command_topic, json.dumps(play_payload))

    # Wait for a short time to allow the message to be sent
    client.loop_start()
    client.loop_stop()

    for lamp in list_of_lights:
        # Topic for publishing commands to Zigbee2MQTT
        mqtt_command_topic = f"zigbee2mqtt/{lamp}/set"  # Replace with your device's topic

        turn_on_payload = {
            "state": "ON",
        }

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(mqtt_broker_address, mqtt_broker_port, 60)

        client.publish(mqtt_command_topic, json.dumps(turn_on_payload))

        # Wait for a short time to allow the message to be sent
        client.loop_start()
        client.loop_stop()

    return render(request, "FDjango/clock.html")

def turn_off_light_all(request):
    mqtt_broker_address = "test.mosquitto.org"
    mqtt_broker_port = 1883

    list_of_lights = ["0xd87a3bfffe0f2231", "0x5cc7c1fffe355388"]
    for lamp in list_of_lights:
        # Topic for publishing commands to Zigbee2MQTT
        mqtt_command_topic = f"zigbee2mqtt/{lamp}/set"  # Replace with your device's topic

        turn_off_payload = {
            "state": "ONcd"
                     "",
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

        client.publish(mqtt_command_topic, json.dumps(turn_off_payload))

        # Wait for a short time to allow the message to be sent
        client.loop_start()
        client.loop_stop()

    return render(request, "FDjango/base.html")

def turn_off_light(request):
    mqtt_broker_address = "test.mosquitto.org"
    mqtt_broker_port = 1883
    id = request.GET.get('lightId')

    mqtt_command_topic = f"zigbee2mqtt/{id}/set"  # Replace with your device's topic

    # Payload to adjust brightness and turn on the lamp
    brightness_increase_payload = {
        "state": "OFF",
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

    return render(request, "FDjango/base.html")


def alter_light_all(request):
    mqtt_broker_address = "test.mosquitto.org"
    mqtt_broker_port = 1883
    list_of_lights = ["0xd87a3bfffe0f2231", "0x5cc7c1fffe355388"]

    color = request.GET.get('color')
    brightness = request.GET.get('brightness')
    color = color.lstrip('#')
    if len(color) == 6:
        rgb_tuple = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
    elif len(color) == 8:
        rgb_tuple = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4, 6))
    else:
        raise ValueError("Invalid hex color code")

    # Normalize RGB values to the range [0, 1]
    rgb_normalized = np.array(rgb_tuple) / 255.0
    color = skimage.color.rgb2xyz(rgb_normalized)
    # convert xyz to xy according to windedHero
    colorx = color[0] / (color[0] + color[1] + color[2])
    colory = color[1] / (color[0] + color[1] + color[2])

    for lamp in list_of_lights:

        # Topic for publishing commands to Zigbee2MQTT
        mqtt_command_topic = f"zigbee2mqtt/{lamp}/set"  # Replace with your device's topic

        # Payload to adjust brightness and turn on the lamp
        brightness_increase_payload = {
            "brightness": brightness,  # Adjust brightness value as needed
            "color": {"x": colorx, "y": colory},
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

    return render(request, "FDjango/base.html")


def alter_light(request):
    mqtt_broker_address = "test.mosquitto.org"
    mqtt_broker_port = 1883
    color = request.GET.get('color')
    brightness = request.GET.get('brightness')
    color = color.lstrip('#')
    if len(color) == 6:
        rgb_tuple = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
    elif len(color) == 8:
        rgb_tuple = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4, 6))
    else:
        raise ValueError("Invalid hex color code")

    # Normalize RGB values to the range [0, 1]
    rgb_normalized = np.array(rgb_tuple) / 255.0
    color = skimage.color.rgb2xyz(rgb_normalized)
    # convert xyz to xy according to windedHero
    colorx = color[0] / (color[0] + color[1] + color[2])
    colory = color[1] / (color[0] + color[1] + color[2])

    # Topic for publishing commands to Zigbee2MQTT
    mqtt_command_topic = f"zigbee2mqtt/{request.GET.get('lightId')}/set"  # Replace with your device's topic

    # Payload to adjust brightness and turn on the lamp
    brightness_increase_payload = {
        "brightness": brightness,  # Adjust brightness value as needed
        "color": {"x": colorx, "y": colory},
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

    return render(request, "FDjango/base.html")


