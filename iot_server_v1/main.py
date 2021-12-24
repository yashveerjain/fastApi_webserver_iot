# print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))

from typing import List

from fastapi import FastAPI,Depends,HTTPException
import uvicorn

from db_handler import universal_apis,admin_apis
from routers import authorization
from internal import admin

app = FastAPI()

app.include_router(universal_apis.router)
app.include_router(admin_apis.router)
app.include_router(authorization.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

if __name__=="__main__":
    uvicorn.run("main:app",host="0.0.0.0", reload=True)