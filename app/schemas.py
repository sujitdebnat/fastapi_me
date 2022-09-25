import email
import imp
from lib2to3.pgen2 import token
from operator import le
from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic import conint

# from app.routers.vote import vote

class PostBase(BaseModel):
    title:str
    content:str
    publish:bool=True


class PostCreat(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode = True

class Post(PostBase):
    id:int
    creted_at:datetime
    owner_id:int
    owner:UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class UserCreat(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)