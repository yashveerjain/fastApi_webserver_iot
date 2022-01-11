from typing import List

from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session

from db_handler import crud,schemas
from dependencies import get_db

router = APIRouter()


@router.post("/admin/user",response_model=schemas.User)
def create_user(user : schemas.UserCreate,db : Session=Depends(get_db)):
    db_user = crud.get_user(db, user_id=1)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered and there is admin")
    
    return crud.create_user(db,user,isadmin=True)


@router.post("/admin")
async def update_admin():
    return {"message": "Admin getting schwifty"}