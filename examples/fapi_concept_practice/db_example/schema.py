"""
To avoid confusion between the SQLAlchemy models and the Pydantic models, 
we will have the file models.py with the SQLAlchemy models, and the file schemas.py with
the Pydantic models.

These Pydantic models define more or less a "schema" (a valid data shape).
So this will help us avoiding confusion while using both.
"""

from typing import List, Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True

    """
    Pydantic's orm_mode will tell the Pydantic model to read the data even 
    if it is not a dict, but an ORM model (or any other arbitrary object with attributes).

    This way, instead of only trying to get the id value from a dict, as in:
    id = data["id"]

    it will also try to get it from an attribute, as in:
    id = data.id

    And with this, the Pydantic model is compatible with ORMs, and you can just declare it in the response_model argument in your path operations.
    You will be able to return a database model and it will read the data from it
    """