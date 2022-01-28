from hashlib import new
from pydantic import FilePath
from sqlalchemy.orm import Session
from fastapi import  Response, status, HTTPException
import os
from Storage.repository.authentication import authenticate, check_password
from .. import schemas, models
from .. hashing import Hash
import shutil


#CREATE A NEW USER.
def create(request:schemas.User, db:Session):
    
    user_exists = db.query(models.User).filter(models.User.email == request.email).first()
    #IF THE USER EXISTS IN THE POSTGRES DATABASE.
    if user_exists:
        print("THE USER ALREADY EXISTS!")
        raise HTTPException(status_code=409, detail = f"EMAIL ID {request.email} has already been taken!")

    #IF THE USER DOES NOT EXIST IN THE POSTGRES DATABASE.
    else:
        new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

# GET ALL USERS.
def get_all_user(db:Session):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with ID {id} not found in our DB')
    return users

#DELETE USER
def delete_user(username:str, password:str, password_confirmation:str, db:Session):    
    #verify if correct password was entered
    if(password!=password_confirmation):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Entered passwords do not match!")
    
    user = db.query(models.User).filter(models.User.email == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with EMAIL {username} was not found in our DB!")

    if not check_password(user,username,password, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Incorrect passwords!")
    
    #DELETE FROM DATABASE
    db.query(models.User).filter(models.User.email == username).delete(synchronize_session=False)
    db.commit()

    #DELETE USER'S FOLDER FROM DISK
    try:
        filePath=f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{username}"
        
        shutil.rmtree(filePath)
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Deleted {username}'s files and account from disk and database")
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Something went wrong while deleting the user's files from the disk")
