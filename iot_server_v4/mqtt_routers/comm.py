from main import mqtt

import logging

def publish(TOPIC,mess_string):
    
    logging.debug(f"{TOPIC} | {mess_string}")
    
    mqtt.publish(TOPIC, mess_string) #publishing mqtt topic 
    return {"result": True,"message":"Published" }
