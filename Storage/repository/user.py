from pydantic import FilePath
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from dotenv import load_dotenv
from Storage.repository.authentication import authenticate, check_password
from .. import schemas, models
from ..hashing import Hash

# Load environment variables
load_dotenv()
filePath = os.getenv("BASE_FILE_DIR")


# CREATE A NEW USER
def create(request: schemas.User, db: Session):
    user_exists = db.query(models.User).filter(models.User.email == request.email).first()

    # IF THE USER EXISTS IN THE POSTGRES DATABASE
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"EMAIL ID {request.email} has already been taken!")

    # IF THE USER DOES NOT EXIST IN THE POSTGRES DATABASE
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    folder = request.email
    try:
        os.makedirs(f"{filePath}/{folder}")  # Ensure user's folder is created
        os.makedirs(f"{filePath}/{folder}_trash")  # Create trash folder for the user
        return new_user

    except OSError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Folder creation failed for user {request.email}: {e.strerror}")


# GET ALL USERS
def get_all_user(db: Session):
    users = db.query(models.User).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No users found in the database')
    
    return users


# DELETE USER
def delete_user(username: str, password: str, password_confirmation: str, db: Session):
    # VERIFY IF THE CORRECT PASSWORD WAS ENTERED
    if password != password_confirmation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Entered passwords do not match!")
    
    user = db.query(models.User).filter(models.User.email == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with EMAIL {username} not found in the database!")
    
    # VERIFY IF THE PASSWORD IS CORRECT
    if not check_password(user, username, password, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password!")
    
    # DELETE USER FROM DATABASE
    db.query(models.User).filter(models.User.email == username).delete(synchronize_session=False)
    db.commit()

    # DELETE USER'S FOLDER AND TRASH FROM DISK
    try:
        shutil.rmtree(f"{filePath}/{username}")  # Delete user folder
        shutil.rmtree(f"{filePath}/{username}_trash")  # Delete user's trash folder
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=f"Deleted {username}'s files and account from disk and database")
    
    except OSError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting user files: {e.strerror}")
