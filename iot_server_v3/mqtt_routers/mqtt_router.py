import asyncio
import signal
from fastapi import APIRouter,Depends,HTTPException
from fastapi.websockets import WebSocket
import logging

from sqlalchemy.orm import Session
import sys

from dependencies import get_db
from . import mqtt_handler
from routers.authorization import verify_token
from db_handler import crud

router = APIRouter(
    dependencies = [Depends(verify_token)]
)


logging.basicConfig(level=logging.DEBUG)

def signal_handler(sig, frame):
    logging.info('You pressed Ctrl+C!')
    sys.exit(0)

@router.websocket("/device/status")
async def update_device_status(websocket : WebSocket,db : Session = Depends(get_db)):
    await websocket.accept()
    internal_queue = asyncio.queues.Queue()
    
    signal.signal(signal.SIGINT, signal_handler)
    
    async def recieve_mess(websocket : WebSocket,int_queue : asyncio.Queue()):
        from mqtt_routers import comm
        while True:
            data = await websocket.receive_json()
            logging.debug(f"recived data : {data}")        
            topic = data["topic_name"]
            mess = data["status"]
            
            result = comm.publish(topic,mess)
            int_queue.put_nowait(data)
            
            # print(data)
            
    
    res_task = asyncio.create_task(recieve_mess(websocket,internal_queue))
    while True:
    
        recieve_status_data = await mqtt_handler.mqtt_handler.send_message()
        if not recieve_status_data:
            continue
        if not internal_queue.empty():
            ## to get the element which was recently recieved and published need not to be send again
            elem_rec = internal_queue.get_nowait()
            logging.debug(f"recieve element not sending : {elem_rec}")
            continue
        
        db_device = crud.get_device_by_topic(db,recieve_status_data["topic_name"])
        if not db_device:
            raise HTTPException(status_code=400, detail="device not found")
        
        db_device = crud.update_device_status(db,device_topic_name=recieve_status_data["topic_name"],status=recieve_status_data["status"])
        logging.debug("Sending message")
        await websocket.send_json(recieve_status_data)
        logging.debug(f"send message {recieve_status_data}")            # 
    
# @router.websocket_route("/device/status")
# class update_device_status(WebSocketEndpoint):
#     encoding = 'json'
#     monitor_message = {"topic_name" : "","status" : ""}


#     async def send_device_status(self, websocket : WebSocket):
#         while True:
#             # print(mqtt_handler.mqtt_handler.send_message())            
#             # recieve_status_data = await mqtt_handler.mqtt_handler.send_message(mqtt_handler.async_queue)
#             # try:
#             recieve_status_data = await mqtt_handler.async_queue.get()
#             # except Exception as e:
#             #     # print(e)
#             #     continue

            
#             # recieve_status_data = await mqtt_handler.mqtt_handler.active_client_message.get()
#             # print("before : ",recieve_status_data)
#             # if not recieve_status_data:
#             #     continue
#             print("after : ",  recieve_status_data)
#             # if self.monitor_message["topic_name"]==recieve_status_data["topic_name"] and self.monitor_message["status"] == recieve_status_data["status"]:
#             #     continue
#             # if recieve_status_data:
#             await websocket.send_json(recieve_status_data)
#             print("prev message",recieve_status_data)

#     async def on_connect(self, websocket):
#         await websocket.accept()
#         # self.TASK = asyncio.create_task(self.send_device_status(websocket,))
#         # signal.signal(signal.SIGINT, signal_handler)
#         while True:
#             # print(mqtt_handler.mqtt_handler.send_message())            
#             # recieve_status_data = await mqtt_handler.mqtt_handler.send_message(mqtt_handler.async_queue)
#             # try:
#             recieve_status_data = await mqtt_handler.async_queue.get()
#             # except Exception as e:
#             #     # print(e)
#             #     continue

            
#             # recieve_status_data = await mqtt_handler.mqtt_handler.active_client_message.get()
#             # print("before : ",recieve_status_data)
#             # if not recieve_status_data:
#             #     continue
#             print("after : ",  recieve_status_data)
#             # if self.monitor_message["topic_name"]==recieve_status_data["topic_name"] and self.monitor_message["status"] == recieve_status_data["status"]:
#             #     continue
#             # if recieve_status_data:
#             await websocket.send_json(recieve_status_data)
#             print("prev message",recieve_status_data)
            
#     async def on_receive(self, websocket, data):
#         from mqtt_routers import comm
#         # print("recived data",data)        
#         topic = data["topic_name"]
#         mess = json.dumps({"status" : data["status"]})
#         self.monitor_message = {"topic_name" : topic, " status" : data["status"]}
        
#         result = comm.publish(topic,mess)

#     async def on_disconnect(self, websocket, close_code):
#         self.TASK.cancel()
#         print("disconnected connection")
#         pass
