# print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))

from sqlalchemy.orm import Session, load_only
from sqlalchemy.sql.functions import mode
from passlib.context import CryptContext

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

## create

def create_user(db: Session, user: schemas.UserCreate, isadmin:bool):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email = user.email,username=user.username,hashed_password = hashed_password,isadmin=isadmin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_device(db : Session, device: schemas.DeviceCreate):
    # print(device.dict())
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


## read
def get_user(db: Session, user_id : int):
    return db.query(models.User).filter(models.User.id==user_id).first()

def get_user_by_email(db: Session, email : str):
    return db.query(models.User).filter(models.User.email==email).first()


def get_device(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id==device_id).first()

def get_device_by_topic(db: Session, device_topic_name: str):

    return db.query(models.Device).filter(models.Device.topic_name==device_topic_name).first()


def get_devices(db: Session):
    devices = db.query(models.Device).all()
    return devices


##update
def update_device_status(db: Session, device_id: int,status: bool):
    db_device = db.query(models.Device).filter(models.Device.id==device_id).first()
    db_device.status = status
    db.commit()
    return db_device

## delete 
def delete_device(db: Session,device_id:int):
    device = db.query(models.Device).filter(models.Device.id==device_id).first()
    db.delete(device)
    db.commit()
    return device

def delele_all_devices(db:Session):
    devices = db.query(models.Device).all()
    # D = []
    for device in devices:    
        db.delete(device)
        # D.append(device)
    db.commit()
    return devices

def delete_user(db:Session,user_id: int):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    db.delete(user)
    db.commit()
    return user



