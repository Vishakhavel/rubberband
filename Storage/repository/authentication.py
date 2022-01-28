
from http.client import HTTPException
from urllib import request
from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
from .. hashing import Hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..repository import authentication

# LOGIC AUTHENTICATE USER
def authenticate(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with EMAIL {request.username} was not found in our DB")

    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Incorrect password")

    access_token = token.create_access_token(
        data={"sub": user.email})

    user_id = user.id
    email = user.email
# RETURNING THE USER'S EMAIL, TOKEN AND ID.
    return {"access_token": access_token, "token_type": "bearer", "user_id": user_id, "email":email} 


#LOGIC TO CHECK PASSWORD.
def check_password(user:schemas.User ,username:str,password:str, db:Session):
    
    if not Hash.verify(user.password, password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Incorrect password!")
    else:
        return True
    


