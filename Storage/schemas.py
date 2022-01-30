from code import interact
import email
from pydantic import BaseModel, BaseSettings
from typing import List, Optional
from Storage.database import Base

class User_id(BaseModel):
    user_id:int

class User(BaseModel):
    name:str
    email:str
    password:str


class ShowUser(BaseModel):
    name:str
    email:str
    id: int

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class ID(BaseModel):
    id:int

class FileName(BaseModel):
    file_name:str

class Email(BaseModel):
    email:str

class RenameFiles(BaseModel):
    email:str
    oldName: str
    newName: str

class viewAllFiles(BaseModel):
    id:int
    email:str

class deleteFile(BaseModel):
    id:int
    email:str
    filename:str

class shareFile(BaseModel):
    sender: str
    reciever: str
    filename:str

class downloadFile(BaseModel):
    id:int
    email:str
    filename:str

class deleteUser(BaseModel):
    username:str
    password: str
    password_confirmation: str


# env vars

class Settings(BaseSettings):
    ...

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
