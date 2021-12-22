"""
It has user, which will make the file working
"""

"""
But in this case, the same FastAPI application will handle the API and the authentication.

So, let's review it from that simplified point of view:

    The user types the username and password in the frontend, and hits Enter.
    The frontend (running in the user's browser) sends that username and password to a specific URL in our API (declared with tokenUrl="token").
    The API checks that username and password, and responds with a "token" (we haven't implemented any of this yet).
        A "token" is just a string with some content that we can use later to verify this user.
        Normally, a token is set to expire after some time.
            So, the user will have to log in again at some point later.
            And if the token is stolen, the risk is less. It is not like a permanent key that will work forever (in most of the cases).
    The frontend stores that token temporarily somewhere.
    The user clicks in the frontend to go to another section of the frontend web app.
    The frontend needs to fetch some more data from the API.
        But it needs authentication for that specific endpoint.
        So, to authenticate with our API, it sends a header Authorization with a value of Bearer plus the token.
        If the token contains foobar, the content of the Authorization header would be: Bearer foobar.

User info 
OAuth2 specifies that when using the "password flow" (that we are using) the client/user must send a username and password fields as form data.

And the spec says that the fields have to be named like that. So user-name or email wouldn't work.

"""

from typing import Dict, Optional
from fastapi import FastAPI,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
from pydantic import BaseModel

###Basic security

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
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


outh2_scheme = OAuth2PasswordBearer(tokenUrl="token")

##creating sample user
class User(BaseModel):
    username : str
    email : Optional[str] = None
    full_name : Optional[str] = None
    disabled : Optional[bool] = None

class UserInDB(User):
    hashed_password : str

def get_current_user(db : Dict, token : str ):
    D = db.get(token)
    if D is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return User(**D) # currently token is username

def fake_hash_password(password):
    return "fakehashed"+password



@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    print(user_dict)
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    print(hashed_password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    ## return dict must always contain the below keys 
    """
    The response of the token endpoint must be a JSON object.

    It should have a token_type. In our case, as we are using "Bearer" tokens, the token type should be "bearer".

    And it should have an access_token, with a string containing our access token.
    """
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/user/me")
async def get_user(token : str = Depends(outh2_scheme)):
    return get_current_user(fake_users_db,token)

if __name__ == "__main__":
    uvicorn.run("fapi_security_2:app",reload = True)

