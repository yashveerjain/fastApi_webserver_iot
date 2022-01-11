"""
paste this in the amazon skill set in json editor, amazon_flask_alexa_v2_skills.json

"""

import logging
import os
 
from flask import Flask
from flask_ask import Ask, request, session, question, statement
# import RPi.GPIO as GPIO
 
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)
 
STATUSON = ["on", "switch on", "enable", "power on", "activate", "turn on"] # all values that are defined as synonyms in type
STATUSOFF = ["off", "switch off", "disactivate", "turn off", "disable", "turn off"]
 
@ask.launch
def launch():
    speech_text = 'Welcome to the Raspberry Pi alexa automation.'
    return question(speech_text)#.reprompt(speech_text).simple_card(speech_text)
 
@ask.intent('LightIntent', mapping = {'status':'st'})
def Gpio_Intent(status,room):
    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(17,GPIO.OUT)
    main_status = status.split()[0]
    if main_status in STATUSON:
        # GPIO.output(17,GPIO.HIGH)
        print("pin is high")
        return statement('Light was turned on')
    elif main_status in STATUSOFF:
        # GPIO.output(17,GPIO.LOW)
        print("pin low")
        return statement('Light was turned off')
    else:
        return statement('Sorry, this command is not possible.')
 
@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text)#.reprompt(speech_text).simple_card('HelloWorld', speech_text)
 
 
@ask.session_ended
def session_ended():
    return "{}", 200
 

if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
 