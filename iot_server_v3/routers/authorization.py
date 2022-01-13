# print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm.session import Session
from fastapi import APIRouter,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt


from db_handler import crud,schemas
from dependencies import get_db

###Basic security

SECRET_KEY = "ae82c7d1bdef6f4eab178c4915c295f0217f5eff7c2b1d78f20ff0c7dcc8fdb1"
ALGORITHM = "HS256"

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


def create_access_token(data: dict, expires_delta : Optional[timedelta]):
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = timedelta(minutes=15)
        exp = datetime.utcnow()+expires_delta
    else:
        exp = datetime.utcnow()+expires_delta
    
    to_encode.update({"exp" : exp})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

def verify_token(token =Depends(oauth2_schema)):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # print(token)
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        # print(payload)
        email : str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return email

def get_current_active_user(email : str =Depends(verify_token),db: Session=Depends(get_db)):
    user = crud.get_user_by_email(db,email)
    if not user:
        raise HTTPException(status_code=400, detail="token is not working change to another user")    
    return user


def authenticate_user(email:str,password : str,db : Session):
    # print(db)
    user = crud.get_user_by_email(db,email)
    if not user:
        return False
    else:
        if not pwd_context.verify(password,user.hashed_password):
            return False
        return user



class RoleChecker:
    ## check if the current user is admin
    def __call__(self, user: schemas.User = Depends(get_current_active_user)):
        if not user.isadmin:
            # logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")

    
@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),db : Session=Depends(get_db)):
    user = authenticate_user(form_data.username,form_data.password,db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")    
    
    user_new = {"sub" : form_data.username}
    expire_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    acc_token = create_access_token(data=user_new,expires_delta=expire_delta)
    
    token_model = schemas.Token(access_token = acc_token,
                        token_type = "bearer")

    ## return dict must always contain the below keys 
    """
    The response of the token endpoint must be a JSON object.

    It should have a token_type. In our case, as we are using "Bearer" tokens, the token type should be "bearer".

    And it should have an access_token, with a string containing our access token.
    """
    # print(token_model)
    return token_model


