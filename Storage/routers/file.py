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

# @router.post("/upload/{email}")
# async def create_upload_file(email:str,file: UploadFile = File(...), queryParams: Optional[str] = None):
#     print(email)
#     return files.upload_file(email,file)
    # print(queryParams)
    # if queryParams:
    #     return queryParams

    # print(queryParams.email)
    # return {"filename": file.filename}

# @router.post("/upload/")
# async def create_upload_file(uploaded_file: UploadFile = File(...), current_user: schemas.User = Depends(get_current_user), q: Optional[str] = None):
   
#     # email = db.query(models.User).filter(models.User.id == request.id).first()
#     # print(email)

 
#     print(q.email)
#     return {"filename":uploaded_file.filename}
    # return file.upload(email, uploaded_file)


    # return file.upload(email,uploaded_file)
  
    # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{id}/{uploaded_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(uploaded_file.file.read())
    # return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}

    # return file.upload_file()


@router.post("/upload/{email}")
async def create_upload_file(email:str,file: UploadFile = File(...), queryParams: Optional[str] = None):
    print(email)
    return files.upload_file(email,file)
    

@router.post("/compress/upload/{email}")
async def create_upload_file(email:str,file: UploadFile = File(...), queryParams: Optional[str] = None):
    print(email)
    return files.zip_upload_file(email,file)

    # email = email[1:-1]

    # # testing zip file
    # path = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}"

    # with zipfile.ZipFile('files.zip', 'w') as my_zip:
    #     my_zip.write(os.path.join(path, "Cloudwiry Hackathon_file.pdf"))
    


    # filename = "Cloudwiry Hackathon_file.pdf"
    # original = "file_zip"
    # # original = os.path.join(filePath, f"{sender}/{filename}")
    # target = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/{filename}"
    # # target = os.path.join(filePath, f"{reciever}/{filename}")
    # shutil.copyfile(original, target)

    # os.remove("")
    # return files.upload_file(email,file)

    



@router.get("/view")
async def view_all_files(request: schemas.viewAllFiles,current_user: schemas.User = Depends(get_current_user) ):
    return files.show_files(request.email)
    # return os.listdir("/Users/roviros/Desktop/files_uploaded_cloudwiry/")



@router.post("/share")
async def create_upload_file(request:schemas.shareFile):
    

    sender = request.sender
    reciever = request.reciever
    filename=request.filename

    print(reciever)
    print(sender)

    # reciever = request.reciever
    # sender =  request.sender
    # print(request.sender)
    return files.share_file(sender,reciever,filename)


@router.delete("/delete")
async def delete_existing_file(request:schemas.deleteFile, current_user: schemas.User = Depends(get_current_user)):
    email = request.email
    filename=request.filename
    return files.delete_file(filename,email)
    # os.remove("/Users/roviros/Desktop/files_uploaded_cloudwiry/") 
    # return "deleted!"



@router.put("/rename")
async def rename_existing_file(request: schemas.RenameFiles, current_user: schemas.User = Depends(get_current_user)):
    old_name = request.oldName
    new_name = request.newName
    email = request.email
    return files.rename_file(email,old_name,new_name)


    # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{uploaded_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(uploaded_file.file.read())
    # return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}


@router.get("/download", response_class=FileResponse)
async def download_file(request:schemas.deleteFile, current_user: schemas.User = Depends(get_current_user)):
    # id = request.id
    email = request.email
    filename = request.filename
    return files.download_file(email,filename)

    # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{uploaded_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(uploaded_file.file.read())
    # return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}




    #TESTING FILE DOWNLOAD

@router.get('/test/download', response_class=FileResponse)
async def download_test_file(request:schemas.downloadFile, current_user: schemas.User = Depends(get_current_user)):
    id = request.id
    email = request.email
    filename = request.filename
    return files.download_file(id,email,filename)


@router.get("/test/files/download/")
async def sample():
    email = "vichu@gmail.com"
    file_list = os.listdir(f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}")
    # file_list = ['E:\\files\image_1.jpg', 'E:\\files\image_2.jpg',
    #                 'E:\\files\image_3.jpg', 'E:\\files\image_4.jpg',
    #                 'E:\\files\image_5.jpg']

    append_str = "/Users/roviros/Desktop/files_uploaded_cloudwiry/"
    file_list_new = [append_str + sub for sub in file_list]

    print(file_list_new)

    with zipfile.ZipFile('final_archive.zip', 'w') as zip:
        for file in file_list:
            zip.write(file, compress_type=zipfile.ZIP_DEFLATED)



# @router.get("/download", )
# async def download(request: schemas.deleteFile, current_user: schemas.User = Depends(get_current_user)):

#     email = request.email
#     filename = request.filename
#     return files.download_file(email,filename)
#     # return FileResponse(f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/OneDrive_1_1-12-2022.zip")


# @router.get("/files/zip")
# async def zipper():
#     zip_filename = "archive.zip"
#     s = io.BytesIO()
#     zf = zipfile.ZipFile(s, "w")
#     for fpath in filenames:
#         # Calculate path for file in zip
#         fdir, fname = os.path.split(fpath)

#         # Add file, at correct path
#         zf.write(fpath, fname)

#     # Must close zip for all contents to be written
#     zf.close()

#     # Grab ZIP file from in-memory, make response with correct MIME-type
#     resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
#         'Content-Disposition': f'attachment;filename={zip_filename}'
#     })

#     return resp