from main import mqtt

import logging

def publish(TOPIC,mess_string):
    
    logging.debug("{TOPIC},{mess_string},{type(mqtt))}")
    
    mqtt.publish(TOPIC, mess_string) #publishing mqtt topic 
    return {"result": True,"message":"Published" }
