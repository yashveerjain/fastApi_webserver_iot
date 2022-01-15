import asyncio
import queue

class mqttHandler():
    def __init__(self,inp_queue=None):
        # self.active_client_message = queue.LifoQueue()
        if inp_queue:
            self.active_client_message = inp_queue
        else:
            # self.active_client_message = asyncio.Queue()
            self.active_client_message = queue.Queue()
        self.message = {}

    def read_message(self,topic,message):
        
        self.active_client_message.put_nowait((topic,message))
    
    async def send_message(self):

        if self.active_client_message.empty():
            await asyncio.sleep(1)
            return {}

        
        k,v = self.active_client_message.get()
        if v=="on" or v=="1" or v=="true":
            v=True
        else:
            v=False

        mess = {
            "topic_name" : k,
            "status" : v
        }
        
        return mess
    
mqtt_handler = mqttHandler()