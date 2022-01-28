from http.client import HTTPException
from urllib import request
from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
from .. hashing import Hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..repository import authentication
from fastapi.responses import JSONResponse

# INITIALIZING ROUTER.
router = APIRouter(
     tags=['Authentication']
)

# LOGIN ROUTE
@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    return authentication.authenticate(request,db)

#LOGOUT ROUTE.
@router.post('/logout')
def logout():
    # HERE WE HAVE NO REPOSITORY FUNCTION ASSOCIATED BECAUSE USER IS LOGGED OUT FROM THE FRONTEND.
    return JSONResponse(status_code=status.HTTP_200_OK, content=f"Successfulyy logged out! Please Login again to continue using the application")