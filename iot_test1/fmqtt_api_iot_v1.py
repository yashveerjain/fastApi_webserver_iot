"""
details are present in :
https://docs.google.com/document/d/1t5qNqFk1zkpqU8hp0CfM5sPngBX_D-aD8vrElaOjCCc/edit
"""

from fastapi import FastAPI,Request
import logging
from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

from fastapi_mqtt import FastMQTT,MQTTConfig
import json

# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main')  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.


# Global variables
LED_GPIO_PIN = 21
led = None # PWMLED Instance. See init_led()
state = {                                                                            # (6)
    'level': 50 # % brightless of LED.
}

app = FastAPI()

#refer https://docs.google.com/document/d/1t5qNqFk1zkpqU8hp0CfM5sPngBX_D-aD8vrElaOjCCc/edit
# for password and username creation 
mqtt_config = MQTTConfig(
    username="iot_test_v1",
    password="yashveer"
)

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)

MQTT_SUB_TOPIC="testing_mqtt/mqtt_sub"
MQTT_PUB_TOPIC="testing_mqtt/mqtt_pub"

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index_api_client.html",{"request" : request,"pin":LED_GPIO_PIN})

class LedStatus(BaseModel):
    level : int

@app.post("/led")
async def led_post(led_status: LedStatus):
    # print(led_status)
    global state
    new_state = led_status.dict()
    # print(new_state)
    state = new_state

    ## important mqtt.publish must be in async function
    mqtt.publish(MQTT_PUB_TOPIC, json.dumps(state),qos=2) #publishing mqtt topic 
    return led_status


@app.get("/led")
def led_get():
    # mqtt.publish(MQTT_TOPIC, json.dumps(state),qos=1) #publishing mqtt topic 
    return state

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe(MQTT_SUB_TOPIC,qos=1) #subscribing mqtt topic 
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    # print("payload type",type(payload))
    print(f"Received message: topic : {topic}, message: {payload.decode()}, qos : {qos}, properties : {properties}")
    print(json.loads(payload.decode()))
    return 0

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

if __name__=="__main__":
    uvicorn.run("fmqtt_api_iot_v1:app",reload=True)