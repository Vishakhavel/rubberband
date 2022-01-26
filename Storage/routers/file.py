from urllib import request
from Storage.oauth2 import get_current_user
from fastapi import APIRouter, FastAPI, Request, Response, status, Depends, HTTPException, File, UploadFile
from typing import List
from .. import schemas #from one directory up in the tree, we're importing the schemas file, that's the double dot.
from .. import database
from .. import models
from .. import oauth2
from ..repository import file
from sqlalchemy.orm import Session
import os

router = APIRouter(
    tags=['Files'],
    prefix ="/file"
)

get_db = database.get_db




# @router.get('/getAllFilesOfUser/{id}',status_code=status.HTTP_200_OK, response_model=List[schemas.File])
# def get_files_by_id(id:int, db:Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     return file.getFilesById(id,db)



# @router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowFile])
# def all(db:Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     # print(request)
#     return file.get_all(db)
    

# @router.post('/', status_code=status.HTTP_201_CREATED)
# def create(request: schemas.File, db:Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     return file.create(request,db)

#     #NEED THE CURRENT USER'S ID

# @router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
# def delete_file(id:int, db:Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     return file.destroy(id,db)


# @router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
# def update(id:int,request: schemas.File,  db:Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     return file.update(id,request,db)

# @router.get('/{id}', status_code = status.HTTP_200_OK, response_model =schemas.ShowFile)
# def show(id:int, response: Response, db:Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     return file.get_id(id,db)


@router.post("/upload")
async def create_upload_file(request:schemas.ID,uploaded_file: UploadFile = File(...), current_user: schemas.User = Depends(get_current_user)):
   
    email = db.query(models.User).filter(models.User.id == request.id).first()
    print(email)
 
    # print(email)
    return"email"

    # return file.upload(email,uploaded_file)
  
    # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{id}/{uploaded_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(uploaded_file.file.read())
    # return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}

    # return file.upload_file()


@router.get("/view")
async def view_all_files():
    return file.show_files()
    # return os.listdir("/Users/roviros/Desktop/files_uploaded_cloudwiry/")


@router.post("/share")
async def share_file(uploaded_file: UploadFile = File(...),current_user: schemas.User = Depends(get_current_user)):

    return file.share(uploaded_file)

    # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{id}/{uploaded_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(uploaded_file.file.read())
    # return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}



@router.delete("/delete")
async def delete_existing_file(email_req:schemas.Email, filename_req:schemas.FileName, current_user: schemas.User = Depends(get_current_user)):
    email = email_req.email
    filename=filename_req.file_name
    return file.delete_file(filename,email)
    # os.remove("/Users/roviros/Desktop/files_uploaded_cloudwiry/") 
    # return "deleted!"



@router.put("/rename")
async def rename_existing_file(uploaded_file: UploadFile = File(...), current_user: schemas.User = Depends(get_current_user)):

    return file.rename_file()


    # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{uploaded_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(uploaded_file.file.read())
    # return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}


@router.get("/download")
async def download_file(uploaded_file: UploadFile = File(...), current_user: schemas.User = Depends(get_current_user)):

    return file.download_file()

    # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{uploaded_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(uploaded_file.file.read())
    # return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}
