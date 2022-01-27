from hashlib import new
from sqlalchemy.orm import Session
from fastapi import  Response, status, HTTPException

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
    user_exists = db.query(models.User).filter(models.User.email == username).first()
    
    #verify if correct password was entered
    if(password!=password_confirmation):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Entered passwords do not match!")
        # return "Entered passwords don't match!"
    
    # return "hi"
    return check_password(username,password, password_confirmation, db)
