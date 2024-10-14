
from inspect import formatannotationrelativeto
from pydantic import FilePath
from sqlalchemy.orm import Session
from fastapi import  status, HTTPException, File, UploadFile
from .. import schemas, models
import os
import shutil
from fastapi.responses import JSONResponse, FileResponse
import zipfile
from dotenv import load_dotenv

# READING FROM ENV VARS. THIS WILL BE OVERWRITTEN BY THE ENV VARS SET IN AWS ELASTIC BEANSTALK DASHBOARD.
load_dotenv()  
filePath = os.getenv("BASE_FILE_DIR")
print("file path from env vars: ",filePath)
current_file_path = os.getenv("CURRENT_FILE_PATH")

# LOGIC TO UPLOAD FILE
def upload_file(email:str, uploaded_file: UploadFile = File(...)):
    
    filename = uploaded_file.filename
    zip_filename = uploaded_file.filename.split(".")[0]
    email = email[1:-1]


    file_location=os.path.join(filePath, f"{email}/{uploaded_file.filename}")
    
    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
            

        return {"info": f"file '{uploaded_file.filename}' has been successfully uploaded to your account"}

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Oopss...Something went wrong!")


# LOGIC TO ZIP AND UPLOAD FILE.
def upload_and_zip_file(email:str, uploaded_file: UploadFile = File(...)):
    try:
        print(email)
        print(email[1:-1])
        email = email[1:-1]
        filename = uploaded_file.filename
        zip_filename = uploaded_file.filename.split(".")[0]
        print(zip_filename)
        file_location=os.path.join(filePath, f"{email}/{uploaded_file.filename}")        
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())\

        #ZIPPING THE FILE AND STORING IT.
        zip_file = zipfile.ZipFile(f'{zip_filename}.zip', 'w')
        zip_file.write(f'{filePath}/{email}/{filename}', compress_type = zipfile.ZIP_DEFLATED)
        zip_file.close()
        print("zipped")
        shutil.copy(f'{current_file_path}/{zip_filename}.zip',f'{filePath}/{email}')
        os.remove(f"/{current_file_path}/{zip_filename}.zip")
        os.remove(f'{file_location}')

        return {"info": f"file '{uploaded_file.filename}' saved as '{zip_filename}.zip'"}
    
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Oopss...Something went wrong!")
 

# LOGIC SHOW ALL FILES OF USER.
def show_files(email:str):
    try:
        return os.listdir(f"{filePath}/{email}")

    except:
        print(f"{filePath}/{email}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Oopss...Something went wrong!")
        
# LOGIC TO SHARE FILE WITH OTHER USER BY EMAIL.
def share_file(sender:str,reciever:str,filename:str):
    # try:
    print(sender)
    print(reciever[1:-1])
    print(filename)
    
    original = f"{filePath}/{sender}/{filename}"
    target = f"{filePath}/{reciever}/{filename}"
    try:
        shutil.copyfile(original, target)
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"File shared successfully to {reciever}")
    
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = f"Please check if the filename: '{filename}' and the username of the receiver: '{reciever}' are correct and try again.")
    

# LOGIC TO RENAME THE FILE USING OLD AND NEW NAMES.
def rename_file(email:str,old_name:str,new_name:str):
    sourceFilePath = f"{filePath}/{email}/{old_name}"
    destinationFilePath = f"{filePath}/{email}/{new_name}"

    try:
        os.rename(sourceFilePath, destinationFilePath)
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"File {old_name} successfully renamed to {new_name}")
    
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"This file name was not found in our database!")


# LOGIC TO DOWNLOAD FILE BY NAME.
def download_file(email:str, filename:str):
   
    try:
        file_download_location = f"{filePath}/{email}/{filename}"
        return file_download_location
    
    except:
        # print(filePath)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "This file name was not found in our database!")


# USER DELETES FILE, IT IS MOVED TO TRASH.
def move_to_trash(filename: str, email: str):

    original = f"{filePath}/{email}/{filename}"
    target = f"{filePath}/{email}_trash/{filename}"
    try:
        shutil.copyfile(original, target)
        os.remove(f"{original}")
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"Deleted {filename} file successfully! You can recover this file form the trash anytime.")
    
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = f"This file - '{filename}' doesn't exist in {email}'s account!")



def empty_trash_of_user(email:str):
    empty_trash_file_location = f"{filePath}/{email}_trash/"

    try:
        for files in os.listdir(empty_trash_file_location):
            path = os.path.join(empty_trash_file_location, files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)


        return JSONResponse(status_code=status.HTTP_200_OK, content="Trash is now empty!")

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Trash is already empty!")



def view_trash(email:str):
    try:
        return os.listdir(f"{filePath}/{email}_trash")

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Oopss...Looks like something went wrong from our side!")


def recover_file_from_trash(filename:str, email:str):
    original = f"{filePath}/{email}_trash/{filename}"
    target = f"{filePath}/{email}/{filename}"
    try:
        shutil.copyfile(original, target)
        os.remove(f"{original}")
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"File {filename} recovered successfully")
    
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = f"This file - '{filename}' doesn't exist in {email}'s trash!")
    
