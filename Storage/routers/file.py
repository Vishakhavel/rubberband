import email
from fileinput import filename
from urllib import request, response
import io
from bcrypt import re
from pydantic import FilePath
from Storage.oauth2 import get_current_user
from fastapi import APIRouter, FastAPI, Request, Response, status, Depends, HTTPException, File, UploadFile
from typing import List, Optional
from .. import schemas #from one directory up in the tree, we're importing the schemas file, that's the double dot.
from .. import database
from .. import models
from .. import oauth2
from ..repository import files
from sqlalchemy.orm import Session
import os
from io import BytesIO
import zipfile
import shutil
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


# INITIALIZING ROUTER.
router = APIRouter(
    tags=['Files'],
    prefix ="/file"
)

# DATABASE REFERENCE.
get_db = database.get_db

# UPLOAD FILE.
@router.post("/upload/{email}")
async def upload_file(email:str,file: UploadFile = File(...), queryParams: Optional[str] = None, current_user: schemas.User = Depends(get_current_user)) :
    print(email)
    return files.upload_file(email,file)


@router.post("/zip/upload/{email}")
async def upload_zip_file(email:str,file: UploadFile = File(...), queryParams: Optional[str] = None, current_user: schemas.User = Depends(get_current_user)) :
    print(email)
    return files.upload_and_zip_file(email,file)

    

# VIEW ALL FILES.
@router.get("/view")
async def view_all_files(request: schemas.viewAllFiles,current_user: schemas.User = Depends(get_current_user) ):
    return files.show_files(request.email)
    # return os.listdir("/Users/roviros/Desktop/files_uploaded_cloudwiry/")


# SHARE FILES WITH OTHER USER.
@router.post("/share")
async def create_upload_file(request:schemas.shareFile,current_user: schemas.User = Depends(get_current_user)):
    sender = request.sender
    reciever = request.reciever
    filename=request.filename
    print("RECIEVER: ", reciever)
    print("SENDER: ", sender)
    return files.share_file(sender,reciever,filename)

# DELETE FILE.
@router.delete("/delete")
async def delete_existing_file(request:schemas.deleteFile, current_user: schemas.User = Depends(get_current_user)):
    email = request.email
    filename=request.filename


    return files.move_to_trash(filename, email)



    # return files.delete_file(filename,email)

# @router.delete("/trash/empty")
# async def delete_existing_file(request:schemas.deleteFile, current_user: schemas.User = Depends(get_current_user)):
#     email = request.email
#     filename="trash/"+request.filename

#     return files.delete_file(filename,email)


@router.delete("/trash/empty")
async def empty_trash(request:schemas.Email, current_user: schemas.User = Depends(get_current_user)):
    email = request.email
    return files.empty_trash_of_user(email)


   


# RENAME EXISTING FILE, ALREADY UPLOADED.
@router.put("/rename")
async def rename_existing_file(request: schemas.RenameFiles, current_user: schemas.User = Depends(get_current_user)):
    old_name = request.oldName
    new_name = request.newName
    email = request.email
    return files.rename_file(email,old_name,new_name)

#DOWNLOAD FILE ALREADY UPLOADED.
@router.get("/download", response_class=FileResponse)
async def download_file(request:schemas.deleteFile, current_user: schemas.User = Depends(get_current_user)):
    email = request.email
    filename = request.filename
    return files.download_file(email,filename)



@router.get("/trash/view")
async def view_trash(request:schemas.Email, current_user: schemas.User = Depends(get_current_user)):
    email = request.email
    return files.view_trash(email)

@router.get("/trash/recover")
async def recover_file_from_trash(request: schemas.deleteFile, current_user: schemas.User = Depends(get_current_user)):
    email = request.email
    filename = request.filename

    print(email)
    print(filename)
    return files.recover_file_from_trash(filename, email)