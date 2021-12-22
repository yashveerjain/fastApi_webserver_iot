"""
this is advance version of fapi_security_2.py it contains encrpytions JWT tokens
"""

"""
JWT : for creating tokens
JWT means "JSON Web Tokens".
It's a standard to codify a JSON object in a long dense string without spaces.
python-jose : We need to install python-jose to generate and verify the JWT tokens in Python

Password hashing : for encrypting the password
"Hashing" means converting some content (a password in this case) into a sequence of bytes
(just a string) that looks like gibberish.Whenever you pass exactly the same content 
(exactly the same password) you get exactly the same gibberish.But you cannot convert 
from the gibberish back to the password.
passlib : PassLib is a great Python package to handle password hashes.It supports many secure hashing algorithms and utilities to work with them.The recommended algorithm is "Bcrypt".

"""
from datetime import datetime, timedelta
from typing import Dict, Optional

from fastapi import FastAPI,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
from pydantic import BaseModel

###Basic security
from jose import JWTError, jwt
from passlib.context import CryptContext

app = FastAPI()

# here the OAuth2PasswordBearer will generate token when authenticated
"""
here tokenUrl="token" refers to a relative URL token that we haven't created yet.
 As it's a relative URL, it's equivalent to ./token.

Because we are using a relative URL, if your API was located at https://example.com/, 
then it would refer to https://example.com/token. 

But if your API was located at https://example.com/api/v1/, 
then it would refer to https://example.com/api/v1/token.


"""

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "ae82c7d1bdef6f4eab178c4915c295f0217f5eff7c2b1d78f20ff0c7dcc8fdb1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
outh2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

## token class must have same parameters 
class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    username: Optional[str] = None

##creating sample user
class User(BaseModel):
    username : str
    email : Optional[str] = None
    full_name : Optional[str] = None
    disabled : Optional[bool] = None

class UserInDB(User):
    hashed_password : str

###########
# for encrypting the password

def authenticate_user(db,username : str,password : str):
    user = db.get(username)
    if not user:
        return False
    else:
        if not verify_password(password,user["hashed_password"]):
            return False
        return user

#############

###############
# for gettng token
def create_access_token(data : dict, expires_delta : Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp" : expire})

    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

def get_user(db, username : str):
    us = db.get(username)
    return us

def get_current_user(token : str = Depends(outh2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # print(token)
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        print(payload)
        username : str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception
    
    user = get_user(fake_users_db,username=token_data.username)
    
    if user is None:
        raise credentials_exception

    return user # currently token is username


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = authenticate_user(fake_users_db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user = UserInDB(**user)

    encode_dict = user.dict()

    expire_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    acc_token = create_access_token(data=encode_dict,expires_delta=expire_delta)
    
    token_model = Token(access_token = acc_token,
                        token_type = "bearer")

    ## return dict must always contain the below keys 
    """
    The response of the token endpoint must be a JSON object.

    It should have a token_type. In our case, as we are using "Bearer" tokens, the token type should be "bearer".

    And it should have an access_token, with a string containing our access token.
    """
    print(token_model)
    return token_model

@app.get("/user/me")
async def my_user(user : str = Depends(get_current_user)):
    return user

if __name__ == "__main__":
    uvicorn.run("fapi_security_3:app",reload = True)

