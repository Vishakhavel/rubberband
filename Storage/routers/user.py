from fastapi import APIRouter, FastAPI, Request, status, Depends, HTTPException
from sqlalchemy.orm  import Session
from .. import database, schemas, models
from ..hashing import Hash
from Storage.oauth2 import get_current_user
from ..repository import user
from typing import List
import os

router = APIRouter(
    tags=['Users'],
    prefix="/user"
)
get_db = database.get_db

@router.post('/', response_model = schemas.ShowUser)
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    folder = request.email
    os.mkdir(f'/Users/roviros/Desktop/files_uploaded_cloudwiry/{folder}')
    return user.create(request,db)

    # new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    # return new_user

# @router.get('/{id}', response_model=schemas.ShowUser)
# def get_user(id:int, db:Session = Depends(get_db)):
    
#     return user.get(id,db)


@router.get('/get-all-users', response_model= List[schemas.ShowUser])
def get_all_users_from_db(db:Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.get_all_user(db)