# print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))

from typing import List

from fastapi import FastAPI,Depends,HTTPException
import uvicorn

from db_handler import universal_apis,admin_apis
from routers import authorization,camera_feed
from internal import admin
# import logging

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
# logging.warning('This will get logged to a file')

app = FastAPI()

app.include_router(universal_apis.router)
app.include_router(admin_apis.router)
app.include_router(authorization.router)
app.include_router(admin.router)
app.include_router(camera_feed.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

if __name__=="__main__":
# print()
    uvicorn.run("main:app",host="0.0.0.0")