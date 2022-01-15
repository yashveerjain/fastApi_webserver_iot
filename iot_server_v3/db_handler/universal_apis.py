import json
import logging
from typing import List

from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from fastapi.websockets import WebSocket

from . import crud, models, schemas
from .dataset import engine
from dependencies import get_db
from routers.authorization import verify_token

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    dependencies = [Depends(verify_token)]
)

"""
Our dependency will create a new SQLAlchemy SessionLocal
that will be used in a single request, and then close it once the request is finished.
"""


@router.post("/device/",response_model=schemas.Device)
def create_device(deviceCreate : schemas.DeviceCreate,db : Session=Depends(get_db) ):
    db_device = crud.get_device_by_topic(db,deviceCreate.topic_name)
    # print(db_device)
    if db_device:
        raise HTTPException(status_code=400, detail=f"device with topic name {deviceCreate.topic_name}already present")
    return crud.create_device(db,deviceCreate)

@router.get("/device/{device_id}",response_model=schemas.Device)
def get_device(device_id: int,db : Session=Depends(get_db) ):
    db_device = crud.get_device(db,device_id)
    if not db_device:
        raise HTTPException(status_code=400, detail="device not found")
    return db_device
        
@router.put("/device/{device_id}",response_model=schemas.Device)
def update_device(device_details: schemas.DeviceBase, device_id : int,db : Session=Depends(get_db) ):

    db_device = crud.get_device(db,device_id)
    if not db_device:
        raise HTTPException(status_code=400, detail="device not found")
    
    db_device = crud.update_device(db,device_id=device_id,device=device_details)
    return db_device


@router.get("/devices",response_model = List[schemas.Device])
def read_devices(db:Session=Depends(get_db)):
    devices = crud.get_devices(db)
    if len(devices)==0:
        raise HTTPException(status_code=400, detail="there are no devices")
    return devices