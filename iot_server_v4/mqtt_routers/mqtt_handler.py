import asyncio
import queue
import sqlite3
import os
import logging
import sys

from fastapi import Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from db_handler.dataset import SQLALCHEMY_DATABASE_NAME
from db_handler import crud
from utils import logging_utils


ACTIVITY = "MQTT ROUTER"
LOGLEVEL = os.environ.get("LOGLEVEL", "DEBUG").upper()
logfile = ACTIVITY.strip().replace(" ", "_")
logger = logging.getLogger(logfile)

from logging.handlers import RotatingFileHandler

Rhandler = RotatingFileHandler(f"logs/{logfile}.log", maxBytes=1e8, backupCount=1)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
Rhandler.setFormatter(formatter)
logger.addHandler(Rhandler)
logger.setLevel(LOGLEVEL)
logging.info(f"Running {ACTIVITY}")


class mqttHandler():
    def __init__(self,inp_queue=None):
        # self.active_client_message = queue.LifoQueue()
        if inp_queue:
            self.active_client_message = inp_queue
        else:
            # self.active_client_message = asyncio.Queue()
            self.active_client_message = queue.Queue()
        self.message = {}

        ## TODO database connection is locking so need to use only sqlalchemy database
        self.conn = sqlite3.connect(SQLALCHEMY_DATABASE_NAME,check_same_thread=False)
        logger.info(f"connected to {SQLALCHEMY_DATABASE_NAME}")  
        self.cursor = self.conn.cursor()
    
    def init(self):
        while True:
            self.send_message()

    def read_message(self,topic,message,db : Session=Depends(get_db)):
        k= topic
        v=message

        if v=="on" or v=="1" or v=="true":
            v=True
        else:
            v=False

        mess = {
            "topic_name" : k,
            "status" : v
        }
        try:
            
            prev_dev_detail = self.cursor.execute("SELECT * FROM device WHERE topic_name=?",(k,)).fetchone()

            if prev_dev_detail:
                # prev_dev_detail = (id, device_name , topic_name, status, gpio_pin, extra_details)
                logger.info(f"previous details of device | {prev_dev_detail}")
                if bool(prev_dev_detail[3]) == mess["status"]:
                    logger.info(f"topic name {mess['topic_name']} | has same status | no update")
                    return (prev_dev_detail.topic_name, prev_dev_detail.status)
                self.cursor.execute("UPDATE device SET status=? WHERE topic_name=?",(v,k,)).fetchone()
                self.conn.commit()
                logger.info(f"published topic name {mess['topic_name']} | status updated to {mess['status']}")
            else:
                logger.info(f"not topic is present in DB | {mess}")
                
        except Exception as e:
            logger.error(logging_utils.get_error_message(e, sys.exc_info()))
            
        return (mess["topic_name"],mess["status"])
        
    
mqtt_handler = mqttHandler()