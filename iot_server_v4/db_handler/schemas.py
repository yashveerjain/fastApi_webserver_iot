from typing import Optional
from pydantic import BaseModel


## for user 
class UserBase(BaseModel):
    email : str
    username : str

class UserCreate(UserBase):
    password : str
    isadmin : Optional[bool]= False

class AdminUserCreate(UserCreate):
    isadmin : bool = True

class User(UserBase):
    id : int

    
    ##important note Config must be same that is "C" must be capital
    class Config:
        orm_mode=True

## for devices
class DeviceBase(BaseModel):
    name: str
    topic_name: str
    gpio_pin : int
    
class DeviceCreate(DeviceBase):
    pass

class DeviceStatus(BaseModel):
    topic_name: str
    status : bool

class Device(DeviceBase):
    id : int
    status : bool
    extra_details : Optional[float]

    class Config:
        orm_mode= True


class Token(BaseModel):
    access_token : str
    token_type : str = "Bearer"