from code import interact
import email
from pydantic import BaseModel, BaseSettings
from typing import List, Optional
from Storage.database import Base

# MODEL FOR USER ID.
class User_id(BaseModel):
    user_id:int

# MODEL FOR USER.
class User(BaseModel):
    name:str
    email:str
    password:str

# MODEL TO SHOW USER, AFTER CREATION.
class ShowUser(BaseModel):
    name:str
    email:str
    id: int

    class Config():
        orm_mode = True

# MODEL TO RETURN DATA TO USER AFTER LOGIN.
class Login(BaseModel):
    username: str
    password: str

# MODEL TO SHOW TOKEN.
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

# MODEL TO RETURN ID.
class ID(BaseModel):
    id:int

# MODEL TO RETURN FILENAME.
class FileName(BaseModel):
    file_name:str

# MODEL TO RETURN EMAIL.
class Email(BaseModel):
    email:str

# MODEL TO RENAME FILE.
class RenameFiles(BaseModel):
    email:str
    oldName: str
    newName: str

# MODEL TO VIEW ALL FILES.
class viewAllFiles(BaseModel):
    id:int
    email:str

#MODEL TO DELETE FILE
class deleteFile(BaseModel):
    id:int
    email:str
    filename:str

# MODEL TO SHARE FILE.
class shareFile(BaseModel):
    sender: str
    reciever: str
    filename:str

# MODE TO DOWNLOAD FILE.
class downloadFile(BaseModel):
    id:int
    email:str
    filename:str

# MODEL TO DELETE USER.
class deleteUser(BaseModel):
    username:str
    password: str
    password_confirmation: str


# SETTINGS FOR ENV VARS.
class Settings(BaseSettings):
    ...

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
