from hashlib import new
from pydantic import FilePath
from sqlalchemy.orm import Session
from fastapi import  Response, status, HTTPException
from fastapi.responses import JSONResponse
import os
from Storage.repository.authentication import authenticate, check_password
from .. import schemas, models
from .. hashing import Hash
import shutil
from dotenv import load_dotenv

load_dotenv()
filePath = os.getenv("BASE_FILE_DIR")


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
        folder = request.email
        try:

            os.mkdir(f'{filePath}/{folder}')
            #added trash folder
            os.mkdir(f'{filePath}/{folder}_trash')
            return new_user
        
        except:
            print(f'{filePath}/{folder}')
            email = request.email
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"Folder could not be created for user {email}")

# GET ALL USERS.
def get_all_user(db:Session):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with ID {id} not found in our DB')
    return users

#DELETE USER
def delete_user(username:str, password:str, password_confirmation:str, db:Session):    
    # VERIFY IF THE CORRECT PASSWORD WAS ENTERED
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

    #DELETE USER'S FOLDER AND TRASH FROM DISK
    try:
    
        shutil.rmtree(f"{filePath}/{username}")
        shutil.rmtree(f"{filePath}/{username}_trash")
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=f"Deleted {username}'s files and account from disk and database")
        
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Something went wrong while deleting the user's files from the disk")
