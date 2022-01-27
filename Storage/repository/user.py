from hashlib import new
from pydantic import FilePath
from sqlalchemy.orm import Session
from fastapi import  Response, status, HTTPException
import os
from Storage.repository.authentication import authenticate, check_password
from .. import schemas, models
from .. hashing import Hash

def create(request:schemas.User, db:Session):
    
    user_exists = db.query(models.User).filter(models.User.email == request.email).first()
    #print(user_exists)
    if user_exists:
        print("THE USER ALREADY EXISTS!")
        raise HTTPException(status_code=409, detail = f"EMAIL ID {request.email} has already been taken!")

    else:
        new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

        
    # if user_exists:
    #     print("THE USER ALREADY EXISTS!")
    #     raise HTTPException(status_code=409, detail = f"EMAIL ID {request.email} has already been taken!")

    # else:
    #     db.add(new_user)
    #     db.commit()
    #     db.refresh(new_user)
    #     return new_user

    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    # return new_user


    
    
    # else:
    #     return "This email is already taken!"

    


# def get(id:int, db:Session):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with ID {id} not found in our DB')
#     return user



def get_all_user(db:Session):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with ID {id} not found in our DB')
    return users


def delete_user(username:str, password:str, password_confirmation:str, db:Session):
    # user_exists = db.query(models.User).filter(models.User.email == username).first()
    
    #verify if correct password was entered
    if(password!=password_confirmation):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Entered passwords do not match!")
        # return "Entered passwords don't match!"
    
    # return "hi"

    user = db.query(models.User).filter(models.User.email == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with EMAIL {username} was not found in our DB!")


    if not check_password(user,username,password, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Incorrect passwords!")
    
    #DELETE FROM DATABASE
    db.query(models.User).filter(models.User.email == username).delete(synchronize_session=False)
    db.commit()

    #DELETE FOLDER FROM DISK
    try:
        filePath=f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{username}"
        os.chmod(filePath, 0o777)
        os.rmdir(filePath) 
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Deleted {username}'s files from disk and database")
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Something went wrong while deleting the user's files from the disk")

    # raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail = f"User {username} has been deleted!")
