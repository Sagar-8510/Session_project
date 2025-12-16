
from pydantic import BaseModel,EmailStr

class RegisterSchema(BaseModel):
    name:str 
    email:EmailStr
    password:str
    max_login:int

class BookSchema(BaseModel):
    title:str
    author:str
    description:str
