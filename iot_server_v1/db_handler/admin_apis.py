from typing import List

from sqlalchemy.sql.functions import user

from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from routers.authorization import RoleChecker
from . import crud, models, schemas
from .dataset import engine
from dependencies import get_db

models.Base.metadata.create_all(bind=engine)

## RoleChecker for checking is admin
router = APIRouter(
    dependencies = [Depends(RoleChecker())]
)


@router.post("/user/",response_model=schemas.User)
def create_user(user : schemas.UserCreate,db : Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db,user,isadmin=user.isadmin)

@router.get("/users/{user_id}",response_model=schemas.User)
def read_user(user_id:int,db : Session=Depends(get_db)):
    ## returning user
    db_user = crud.get_user(db,user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user

@router.get("/user/delete/{user_id}")
def delete_user(user_id:int,db:Session=Depends(get_db)):
    db_user = crud.get_user(db,user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return crud.delete_user(db,user_id)


@router.get("/device/delete/{device_id}",response_model=schemas.Device)
def delete_device(device_id : int, db : Session=Depends(get_db)):
    db_device = crud.get_device(db,device_id)
    if not db_device:
        raise HTTPException(status_code=400, detail="device not found")
    return crud.delete_device(db,device_id=device_id)
    
@router.get("/devices/delete",response_model= List[schemas.Device])
def delete_devices(db : Session=Depends(get_db)):    
    devices = crud.delele_all_devices(db)
    if len(devices)==0:
        raise HTTPException(status_code=400, detail="there are no devices")
    print(devices)
    return devices

