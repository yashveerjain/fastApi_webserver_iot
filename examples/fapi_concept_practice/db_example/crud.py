from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from sqlalchemy.sql.type_api import Emulated
from passlib.context import CryptContext

import models, schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email==email).first()

def get_users(db: Session,skip: int =0, limit: int=0):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_items(db: Session, skip: int=0,limit:int=0):
    return db.query(models.Item).offset(skip).limit(limit).all()

"""
Now create utility functions to create data.
The steps are:
    Create a SQLAlchemy model instance with your data.
    add that instance object to your database session.
    commit the changes to the database (so that they are saved).
    refresh your instance (so that it contains any new data from the database, like the generated ID).

"""

def create_user(db: Session, user: schema.UserCreate):
    fake_hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email = user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_item(db: Session, item: schema.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(),owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item