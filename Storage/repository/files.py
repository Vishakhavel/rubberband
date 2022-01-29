
from pydantic import FilePath
from sqlalchemy.orm import Session
from fastapi import  status, HTTPException, File, UploadFile
from .. import schemas, models
import os
import shutil
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
import zipfile

filePath = "/Users/roviros/Desktop/files_uploaded_cloudwiry/"

# LOGIC UPLOAD FILE .
def upload_file(email:str, uploaded_file: UploadFile = File(...)):
    print(email)
    print(email[1:-1])
    email = email[1:-1]
    file_location=os.path.join(filePath, f"{email}/{uploaded_file.filename}")
    
        
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}

# LOGIC SHOW ALL FILES OF USER.
def show_files(email:str):
    try:
        return os.listdir(f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}")

    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail = f"Oopss...Something went wrong!")
        
# LOGIC TO SHARE FILE WITH OTHER USER BY EMAIL,.
def share_file(sender:str,reciever:str,filename:str):
    # try:
    print(sender)
    print(reciever[1:-1])
    print(filename)
    
    original = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{sender}/{filename}"
    target = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{reciever}/{filename}"
    try:
        shutil.copyfile(original, target)
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"File shared successfully to {reciever}")
    
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = f"This file - '{filename}' doesn't exist in {sender}'s account!")
    
# LOGIC TO DELETE FILE BY NAME.
def delete_file(filename:str, email:str):
    try:
        filePath = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/{filename}" #here email and the filename will come
        os.chmod(filePath, 0o777)
        os.remove(f"{filePath}")
        return JSONResponse(status_code=status.HTTP_200_OK, content="Deleted file successfully!")
   
    except: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = f"This file - '{filename}' doesn't exist in {email}'s account!")

# LOGIC TO RENAME THE FILE USING OLD AND NEW NAMES.
def rename_file(email:str,old_name:str,new_name:str):
    sourceFilePath = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/{old_name}"
    destinationFilePath = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/{new_name}"

    try:
        os.rename(sourceFilePath, destinationFilePath)
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"File {old_name} successfully renamed to {new_name}")
    
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"This file name was not found in our database!")


# LOGIC TO DOWNLOAD FILE BY NAME.
def download_file(email:str, filename:str):

    try:
        filePath = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/{filename}"
        return filePath
    
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "This file name was not found in our database!")
