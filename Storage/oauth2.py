from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from . import token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #URL from where the token is gonna be fetched

async def get_current_user(token_value: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}, 
    )
    
    return token.verify_token(token_value, credentials_exception)
