"""
simple short lived client
# from websocket import create_connection
# ws = create_connection("ws://localhost:8000/ws")
# print("Sending 'Hello, World'...")
# while True:
#     data = input()
#     ws.send(f"{data}")
#     print("Sent")
#     print("Receiving...")
#     result =  ws.recv()
#     print("Received '%s'" % result)
# ws.close()
"""

import websocket
import _thread
import time
import json

def on_message(ws, message):
    print("recieve message",message)

def on_error(ws, error):
    print(error)
    # raise "error"

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        i=0
        while True:
            i+=1
            time.sleep(1)
            # ws.send("Hello %d" % i)
            ws.send(json.dumps({"message" : i}))
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    _thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000/ws",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    
    while True:
        try:
            ws.run_forever(ping_interval=2,ping_timeout=1)
        except:
            continue
        