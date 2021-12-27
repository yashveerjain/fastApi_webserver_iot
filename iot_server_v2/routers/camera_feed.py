"""
This file will stream real time video 
"""

import time
from multiprocessing import Process, Queue
import threading

from fastapi import APIRouter,HTTPException,status,Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
import cv2

templates = Jinja2Templates(directory="templates")

router = APIRouter()

class handle_clients:
    def __init__(self):
        self.request_lists = []
        self.cap = None

    def get_capture(self,request:Request):
        if len(self.request_lists)==0:
            # self.cap = imutils.video.VideoStream(src=0).start()
            self.cap = cv2.VideoCapture(0) 
        self.update_requests(request)
        return self.cap

    def update_requests(self,request : Request):
        self.request_lists.append(request)

    def delete_request(self,request:Request):
        self.request_lists.remove(request)
        if len(self.request_lists)==0 and not self.cap==None:
            self.cap.release()
            

manager = handle_clients()

async def get_video(request):
    global cap
    
    start_t = time.time()
    time_count = time.time()-start_t
    if not cap.isOpened():    
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="not able to capture video")
    while cap.isOpened(): #time_count<10:
        ret,frame = cap.read()
        if frame is None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="not able to capture video")
            
        frame = cv2.resize(frame, (680,680))
        output_frame = frame.copy()

        (flag, encodedImage) = cv2.imencode(".jpg", output_frame)
        if not flag:
            continue
        if await request.is_disconnected():
            print("client is disconnected")
            manager.delete_request(request)            
            break
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                        bytearray(encodedImage) + b'\r\n')
        

@router.get("/camera_feed")
async def camera_feed(request:Request):
    global cap
    cap = manager.get_capture(request)
    streamer = get_video(request)
    return StreamingResponse(streamer,media_type="multipart/x-mixed-replace;boundary=frame")

@router.get("/camera")
def index(request: Request):
    return templates.TemplateResponse("camera_frame_fetch.html",{"request":request,"video_url":"/camera_feed"})
