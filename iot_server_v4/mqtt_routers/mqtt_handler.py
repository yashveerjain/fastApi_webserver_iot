import asyncio
import queue
import sqlite3
import os
import logging

from db_handler.dataset import SQLALCHEMY_DATABASE_NAME

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
        self.conn = sqlite3.connect(SQLALCHEMY_DATABASE_NAME)
        logger.info(f"connected to {SQLALCHEMY_DATABASE_NAME}")  
        self.cursor = self.conn.cursor()
    
    def init(self):
        while True:
            self.send_message()

    def read_message(self,topic,message):
        k= topic
        v=message
    #     self.active_client_message.put_nowait((topic,message))
    # def send_message(self):

        # if self.active_client_message.empty():
        #     return 
        
        # k,v = self.active_client_message.get()
        if v=="on" or v=="1" or v=="true":
            v=True
        else:
            v=False

        mess = {
            "topic_name" : k,
            "status" : v
        }
        try:
            ## TODO database connection is locking so need to use only sqlalchemy database
            self.cursor.execute("UPDATE device SET status=? WHERE topic_name=?",(v,k))
            logger.info(f"UPDATE device SET status=? WHERE topic_name=?, {(v,k)}")
            self.conn.commit()
        except Exception as e:
            logger.error(f"""
                    Command NOT Working
                    UPDATE device SET status=? WHERE topic_name=?, {(v,k)}""")
            
        return 
        
    
mqtt_handler = mqttHandler()