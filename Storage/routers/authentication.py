from http.client import HTTPException
from urllib import request
from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
from .. hashing import Hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..repository import authentication


router = APIRouter(
     tags=['Authentication']
)


@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    return authentication.authenticate(request,db)

#     user = db.query(models.User).filter(models.User.email == request.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with EMAIL {request.username} was not found in our DB")

    
#     if not Hash.verify(user.password, request.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Incorrect password")

#     #generate JWT Token and return

#    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     #user_id = request.id

#     access_token = token.create_access_token(
#         data={"sub": user.email})

#     #user_id calculation

#     user_id = user.id
#     print(user_id)

#     return {"access_token": access_token, "token_type": "bearer", "user_id": user_id} #sending the user's ID, and the token.




@router.post('/logout')
def logout():
    return "Successfulyy logged out! Please Login again to continue using the application"