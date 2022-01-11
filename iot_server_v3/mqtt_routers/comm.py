# from fastapi import APIRouter
# from fastapi_mqtt import FastMQTT,MQTTConfig
import logging
from main import mqtt
# # router = APIRouter()

# mqtt_config = MQTTConfig(
#     username="home_automation_v1",
#     password="yashveer"
# )

# mqtt = FastMQTT(
#     config=mqtt_config
# )

# def create_mqtt_instance(router):
#     ## call by main.py to give the app to the mqtt
#     global mqtt
#     mqtt.init_app(router)
     
# SUB_TOPIC="#"

# @mqtt.on_connect()
# def connect(client, flags, rc, properties):
#     mqtt.client.subscribe(SUB_TOPIC) #subscribing mqtt topic 
#     print("Connected: ", client, flags, rc, properties)

# @mqtt.on_message()
# async def message(client, topic, payload, qos, properties):
#     print("Received message: ",topic, payload.decode(), qos, properties)
#     return 0

# @mqtt.on_disconnect()
# def disconnect(client, packet, exc=None):
#     print("Disconnected")

# @mqtt.on_subscribe()
# def subscribe(client, mid, qos, properties):
#     print("subscribed", client, mid, qos, properties)

def publish(TOPIC,mess_string):
    global mqtt
    
    logging.debug("{TOPIC},{mess_string},{type(mqtt))}")
    
    mqtt.publish(TOPIC, mess_string) #publishing mqtt topic 
    return {"result": True,"message":"Published" }

# if __name__=="__main__":
#     pass 
    ##REFER iot_test1/fmqtt_api_iot_v1.py
    # for i in range(5):
    #     mess_string = input()
    
