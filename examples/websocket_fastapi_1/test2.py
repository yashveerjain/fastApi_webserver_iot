from typing import List
from fastapi import FastAPI, WebSocket,WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    encoding = "text"

    def __init__(self):
        self.activeConnections : List = []
        self.receive_text : str = ""

    async def connect(self,websocket:WebSocket):
        await websocket.accept()
        self.activeConnections.append(websocket)

    async def send_personal_message(self,websocket: WebSocket):
        message = self.receive_text
        print(message)
        await websocket.send_text(message)

    async def recieve_message(self,websocket:WebSocket):
        data = await websocket.receive_text()
        self.receive_text= data
    
    async def disconnect(self,websocket :WebSocket):
        self.activeConnections.remove(websocket)

    async def broadcast(self):
        for connections in self.activeConnections:
            await connections.send_text(self.receive_text)



manager = ConnectionManager()


@app.get("/")
def index():
    return HTMLResponse(html)

@app.websocket("/ws/{client_id}")
async def websocket_end_point(client_id: str,websocket: WebSocket):
    await manager.connect(websocket)
    try:
        print(client_id," connected")
        while True:
            await manager.recieve_message(websocket)
            # await manager.broadcast()
            await manager.send_personal_message(websocket)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        print(f"the {client_id} is disconnected")

if __name__=="__main__":
    uvicorn.run("test2:app",reload=True)