from typing import List

from sqlalchemy.sql.functions import user
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
import uvicorn

import crud, models, schema
from dataset import SessionLocal,engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

"""
Our dependency will create a new SQLAlchemy SessionLocal
that will be used in a single request, and then close it once the request is finished.
"""
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}",response_model=schema.User)
def read_user(user_id: int, db: Session=Depends(get_db)):
    db_user = crud.get_user(db,user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schema.Item)
def create_item_for_user(
    user_id: int, item: schema.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schema.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

"""
Here we are using SQLAlchemy code inside of the path operation function and in the dependency,
and, in turn, it will go and communicate with an external database.
That could potentially require some "waiting".
But as SQLAlchemy doesn't have compatibility for using await directly, as would be with
something like:
user = await db.query(User).first()

...and instead we are using:
user = db.query(User).first()

Then we should declare the path operation functions and the dependency without async def,
 just with a normal def
"""

if __name__=="__main__":
    uvicorn.run("main:app",reload=True)