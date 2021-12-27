from fastapi import Depends,HTTPException

from db_handler.dataset import SessionLocal
from db_handler import schemas

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

