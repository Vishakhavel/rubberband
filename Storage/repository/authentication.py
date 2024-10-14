from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .. import schemas, database, models, token
from ..hashing import Hash


# LOGIC TO AUTHENTICATE USER
def authenticate(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Retrieve the user by email
    user = db.query(models.User).filter(models.User.email == request.username).first()
    
    # Check if the user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with EMAIL {request.username} not found"
        )

    # Check if the password is correct
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Generate the access token for the authenticated user
    access_token = token.create_access_token(data={"sub": user.email})

    # Return the access token along with other user information
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "user_id": user.id, 
        "email": user.email
    }


# LOGIC TO CHECK PASSWORD
def check_password(user: schemas.User, username: str, password: str, db: Session):
    # Verify if the provided password matches the stored hash
    if not Hash.verify(user.password, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return True
