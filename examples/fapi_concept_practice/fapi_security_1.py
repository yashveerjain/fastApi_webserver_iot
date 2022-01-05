"""
This file will not give you authorisation but it will glimpse of what needed to be there
to run the authorisation.
Hence it is important file
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

"""

from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordBearer
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
outh2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def index(token: str = Depends(outh2_scheme)):
    print(token)
    ##without user we can not get the token and we will not be able to authorise
    return {"token" : token}


if __name__ == "__main__":
    uvicorn.run("fapi_security_1:app",reload = True)

