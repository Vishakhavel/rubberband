from pydantic import BaseModel
from typing import List, Optional

# class FileBase(BaseModel):
#     title: str
#     body:str
#     user_id: int

# class File(FileBase): #Blog extends BlogBase
 
#     class Config():
#         orm_mode = True


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

    # blogs: List[File] =[]

    class Config():
        orm_mode = True



# class ShowFile(File):
#     title: str
#     body:str
#     creator: ShowUser #since showuser comes before in the line, no error. if this class was defined above the SHowUser, error will be thrown.
#     class Config():
#         orm_mode = True


# class ShowFile(File):
#     title: str
#     body:str
#     id:int
#     # creator: ShowUser #since showuser comes before in the line, no error. if this class was defined above the SHowUser, error will be thrown.
#     # class Config():
#     #     orm_mode = True


# class ShowFileOfUser(File):
#     title: str
#     body: str
#     id:int
#     class Config():
#         orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None