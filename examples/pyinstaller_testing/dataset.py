# from sqlalchemy import *
import sqlalchemy
import passlib

# from fastapi_mqtt import *

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# import fastapi
# from fastapi import FastAPI,Depends,HTTPException
# import uvicorn


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

if __name__ == "__main__":
    print("testing the pyinstaller compilation and printing the sqllite ur",SQLALCHEMY_DATABASE_URL)