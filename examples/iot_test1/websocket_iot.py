from typing import Dict, List
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
import logging
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

# Global variables
LED_GPIO_PIN = 21
led = None # PWMLED Instance. See init_led()
state = {                                                                            # (6)
    'level': 50 # % brightless of LED.
}

app = FastAPI()

class LedStatus(BaseModel):
    level : int

class WebSocketManager:
    encoding = "json"
    
    def __init__(self, ):
        self.activeConnections : List = []
        self.message : LedStatus

    async def connect(self, websocket : WebSocket):
        await websocket.accept()
        self.activeConnections.append(websocket)

    async def recieve_message(self,websocket:WebSocket):
        self.message = LedStatus(**await websocket.receive_json()) ## dict to pydantic
        return self.message
    
    async def send_personal_message(self, websocket:WebSocket,message:Dict):
        await websocket.send_json(message)

    async def broadcast(self):
        for connections in self.activeConnections:
            connections.send_json(self.message)

    async def disconnect(self,websocket:WebSocket):
        await self.activeConnections.remove(websocket)


## this for using js scripts present in  static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index_ws_client_v2.html",{"request" : request,"pin":LED_GPIO_PIN})


manager = WebSocketManager()

# @app.websocket("/")
# async def websocket_endpoints(websocket : WebSocket):
    
    
@app.websocket("/led")
async def handling_status(websocket : WebSocket):
    await manager.connect(websocket)
    try: 
        print("connected device")
        while True:
            data = await manager.recieve_message(websocket)
            print(data)
            state = data.dict()
            await manager.send_personal_message(websocket,state)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        print("disconnected")


if __name__ == "__main__":
    uvicorn.run("websocket_iot:app",reload=True)