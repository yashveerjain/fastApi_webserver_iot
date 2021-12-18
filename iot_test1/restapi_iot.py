from fastapi import FastAPI,Request
import logging
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


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

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index_api_client.html",{"request" : request,"pin":LED_GPIO_PIN})

class LedStatus(BaseModel):
    level : int

@app.post("/led")
def led_post(led_status: LedStatus):
    # print(led_status)
    global state
    new_state = led_status.dict()
    # print(new_state)
    state = new_state
    return led_status

@app.get("/led")
def led_get():
    return state
    