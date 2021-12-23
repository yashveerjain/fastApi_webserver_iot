from fastapi import FastAPI
from fastapi_mqtt import FastMQTT,MQTTConfig


app = FastAPI()

mqtt_config = MQTTConfig()

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)

TOPIC="testing_mqtt/mqtt"


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe(TOPIC) #subscribing mqtt topic 
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    return 0

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


async def func(mess_string):
    mqtt.publish(TOPIC, mess_string) #publishing mqtt topic 
    return {"result": True,"message":"Published" }
if __name__=="__main__":
    pass 
    ##REFER iot_test1/fmqtt_api_iot_v1.py
    # for i in range(5):
    #     mess_string = input()
    
