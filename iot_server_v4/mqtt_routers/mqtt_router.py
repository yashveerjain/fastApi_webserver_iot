import signal
from fastapi import APIRouter,Depends,HTTPException
from fastapi.websockets import WebSocket
import logging
import os

from sqlalchemy.orm import Session
import sys

from dependencies import get_db
from . import mqtt_handler
from routers.authorization import verify_token
from db_handler import crud,schemas

router = APIRouter(
    dependencies = [Depends(verify_token)]
)

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


def signal_handler(sig, frame):
    logger.info('You pressed Ctrl+C!')
    sys.exit(0)


@router.put("/device/{device_id}/status",response_model=schemas.Device)
def update_device_status(device_status: schemas.DeviceStatus,db : Session = Depends(get_db)):
    from mqtt_routers import comm
    
    data = device_status.dict()
    logger.info(f"recived data : {data}")        
    topic = data["topic_name"]
    mess = data["status"]

    prev_dev_detail = crud.get_device_by_topic(db,device_topic_name=data["topic_name"])
    if prev_dev_detail.status == mess:
        logger.info(f"topic name {data['topic_name']} | has same status | no update")
        return prev_dev_detail
    result = comm.publish(topic,mess)
    logger.info(f"publish {result}")
    db_device = crud.update_device_status(db,device_topic_name=data["topic_name"],status=data["status"])
    logger.info(f"topic name {data['topic_name']} | status updated to {data['status']}")
    return db_device

@router.get("/device/{device_id}/status",response_model=schemas.Device)
def get_device_status(device_id : int,db : Session = Depends(get_db)):
    db_device = crud.get_device(db,device_id=device_id)
    return db_device


    # res_task = asyncio.create_task(recieve_mess(websocket,internal_queue))
    # while True:
    
    #     recieve_status_data = await mqtt_handler.mqtt_handler.send_message()
    #     if not recieve_status_data:
    #         continue
    #     if not internal_queue.empty():
    #         ## to get the element which was recently recieved and published need not to be send again
    #         elem_rec = internal_queue.get_nowait()
    #         logger.debug(f"recieve element not sending : {elem_rec}")
    #         continue
        
    #     db_device = crud.get_device_by_topic(db,recieve_status_data["topic_name"])
    #     if not db_device:
    #         logger.error(f"device not found | topic name {recieve_status_data['topic_name']}")
    #         raise HTTPException(status_code=400, detail="device not found")
        
    #     db_device = crud.update_device_status(db,device_topic_name=recieve_status_data["topic_name"],status=recieve_status_data["status"])
    #     logger.debug("Sending message")
    #     await websocket.send_json(recieve_status_data)
    #     logger.debug(f"send message {recieve_status_data}")            # 
    
