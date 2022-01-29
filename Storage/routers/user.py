from fastapi import APIRouter, FastAPI, Request, status, Depends, HTTPException
from sqlalchemy.orm  import Session
from .. import database, schemas, models
from ..hashing import Hash
from Storage.oauth2 import get_current_user
from ..repository import user
from typing import List
import os

# INITIALIZING ROUTER
router = APIRouter(
    tags=['Users'],
    prefix="/user"
)

# DATABASE REFERENCE
get_db = database.get_db


#old EFS file path
# filePath = "/home/ec2-user/efs-mount-point/files"
# os.system("sudo mkdir /ef/files/checker_folder")

#new EFS file path
filePath = "/home/ec2-user/efs-mount-point"



# CREATE A NEW FOLDER WITH THE NEW USER'S EMAIL AS THE NAME.
@router.post('/', response_model = schemas.ShowUser)
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    folder = request.email
    os.mkdir(f'{filePath}/{folder}')
    return user.create(request,db)

    
# GET ALL THE EXISTING USERS FROM THE DATABASE.
@router.get('/get-all-users', response_model= List[schemas.ShowUser])
def get_all_users_from_db(db:Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.get_all_user(db)


#DELETE A SPECIFIC USER FROM THE DATABASE.
@router.delete('/delete')
def delete_user(request:schemas.deleteUser, db:Session=Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    username =  request.username
    password = request.password
    password_confirmation = request.password_confirmation    
    return user.delete_user(username,password,password_confirmation,db)