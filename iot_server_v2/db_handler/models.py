
from .dataset import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Boolean, Float


class User(Base):
    __tablename__ = "user"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,index=True)
    email = Column(String,unique=True,index=True)
    hashed_password = Column(String)

    isadmin = Column(Boolean,default=True)

class Device(Base):
    __tablename__= "device"

    id = Column(Integer,primary_key=True)
    name = Column(String)
    topic_name = Column(String,unique=True)
    status = Column(Boolean,default=False)
    gpio_pin = Column(Integer)

    ## temperature data etc.
    extra_details = Column(Float)





