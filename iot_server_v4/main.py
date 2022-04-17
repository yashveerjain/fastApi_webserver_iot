"""
If server is throwing this error :
File "uvloop/loop.pyx", line 2001, in uvloop.loop.Loop.create_connection
ConnectionRefusedError: [Errno 111] Connection refused

Then mosquitto broker is not running, please check mosquitto broker.
"""
import json
import os
import logging
from typing import List

from fastapi_mqtt import FastMQTT,MQTTConfig
from fastapi import FastAPI,Depends,HTTPException
import uvicorn


from db_handler import universal_apis,admin_apis
from mqtt_routers import mqtt_handler
from routers import authorization,camera_feed
from mqtt_routers import mqtt_router
from internal import admin

import logging

ACTIVITY = "MQTT ROUTER"
LOGLEVEL = os.environ.get("LOGLEVEL", "DEBUG").upper()
logfile = ACTIVITY.strip().replace(" ", "_")
logger = logging.getLogger(logfile)

from logging.handlers import RotatingFileHandler

Rhandler = RotatingFileHandler(f"logs/{logfile}.log", maxBytes=5e8, backupCount=1)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
Rhandler.setFormatter(formatter)
logger.addHandler(Rhandler)
logger.setLevel(LOGLEVEL)
logging.info(f"Running {ACTIVITY}")



app = FastAPI()    

app.include_router(universal_apis.router)
app.include_router(admin_apis.router)
app.include_router(authorization.router)
app.include_router(admin.router)
# app.include_router(camera_feed.router)
app.include_router(mqtt_router.router)


## reference : https://github.com/sabuhish/fastapi-mqtt/blob/master/docs/getting-started.md
mqtt_config = MQTTConfig(
    username="home_automation_v1",
    password="yashveer",
    port=1883
)

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)

SUB_TOPIC="#" ## subscribe to all the topics

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    ## "events" topic is universal topic which will hold the record of all the subscribe and unsubscribe devices
    mqtt.publish("events","main server is connected",qos=2)
    
    ## main server will subscribe to all the topics
    mqtt.client.subscribe(SUB_TOPIC,qos=2) #subscribing mqtt topic 
    
    logger.info(f"Connected: | {client}| {flags} | {rc} | {properties}")

# ## as i have subscribe to all the topics message will keep on display on terminal

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    ## payload will store value like on or off
    payload= payload.decode() # give string format payload
    logger.info(f"payload : {payload} , type: {type(payload)}")
    mqtt_handler.mqtt_handler.read_message(topic,payload)
    return 0


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    mqtt.publish("events","main server is disconnected",qos=2)
    logger.info("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    mqtt.publish("events","main server is subscribed",qos=2)
    logger.info(f"subscribed | {client} | {mid} |  {qos} | {properties}")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__=="__main__":
    # print()    
    uvicorn.run("main:app",host="0.0.0.0")