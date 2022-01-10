from flask import Flask, render_template
from flask_ask import Ask, statement,question

from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi  import FastAPI
import uvicorn

flask_app = Flask(__name__)
ask = Ask(flask_app, '/alexa')

app = FastAPI()
app.mount("/alexa", WSGIMiddleware(flask_app))

@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like to test api?'
    return question(welcome_message)

@ask.intent('YesIntent')
def hello():
    text = render_template('testing is ok')
    return statement(text)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)

@app.get("/")
def index():
    return "HELLO WORLD"

if __name__ == '__main__':
    ## not tested yet
    ## more details on : https://pythonprogramming.net/testing-deploying-alexa-skill-flask-ask-python-tutorial/?completed=/headlines-function-alexa-skill-flask-ask-python-tutorial/
    uvicorn.run("amazon_alexa:app",reload=True,host="0.0.0.0",port=5000)