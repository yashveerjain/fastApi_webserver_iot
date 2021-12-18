"""
This sample paho mqtt code
its only currently capable of only subscribe 
"""

import paho.mqtt.client as mqtt
import sys

TOPIC = "testing_mqtt/mqtt_pub" #sys.argv[1]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode())

client = mqtt.Client()
client.username_pw_set("iot_test_v1", password="yashveer")
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.29.165", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()