
from inspect import formatannotationrelativeto
from pydantic import FilePath
from sqlalchemy.orm import Session
from fastapi import  status, HTTPException, File, UploadFile
from .. import schemas, models
import os
import shutil
from fastapi.responses import JSONResponse, FileResponse
# from fastapi.responses import FileResponse
import zipfile
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

SOME_CONFIG_I_NEED = os.environ.get("SOME_CONFIG_I_NEED")

filePath = "/Users/roviros/Desktop/files_uploaded_cloudwiry"

# LOGIC UPLOAD FILE .
def upload_file(email:str, uploaded_file: UploadFile = File(...)):
    print(email)
    print(email[1:-1])
    email = email[1:-1]
    filename = uploaded_file.filename
    zip_filename = uploaded_file.filename.split(".")[0]
    print(zip_filename)
    print(SOME_CONFIG_I_NEED)  # This will prin



    file_location=os.path.join(filePath, f"{email}/{uploaded_file.filename}")
    
        
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())\
        
    # print(os.ge)

    return {"info": f"file '{uploaded_file.filename}' has been successfully uploaded to your account"}

    
    #ZIPPING THE FILE AND STORING IT.

    # zip_file = zipfile.ZipFile(f'{zip_filename}.zip', 'w')
    # zip_file.write(f'{filePath}/{email}/{filename}', compress_type = zipfile.ZIP_DEFLATED)
    # zip_file.close()
    # print("zipped")
    # shutil.copy(f'/Users/roviros/Desktop/hackathon/{zip_filename}.zip',f'{filePath}/{email}')
    # os.remove(f"/Users/roviros/Desktop/hackathon/{zip_filename}.zip")
    # os.remove(f'{file_location}')

    # return {"info": f"file '{uploaded_file.filename}' saved as '{zip_filename}.zip'"}

    #END OF ZIPPING THE FILE LOGIC.



def upload_and_zip_file(email:str, uploaded_file: UploadFile = File(...)):
    print(email)
    print(email[1:-1])
    email = email[1:-1]
    filename = uploaded_file.filename
    zip_filename = uploaded_file.filename.split(".")[0]
    print(zip_filename)
    file_location=os.path.join(filePath, f"{email}/{uploaded_file.filename}")        
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())\

    # return {"info": f"file '{uploaded_file.filename}' saved as '{zip_filename}'"}
    #ZIPPING THE FILE AND STORING IT.

    zip_file = zipfile.ZipFile(f'{zip_filename}.zip', 'w')
    zip_file.write(f'{filePath}/{email}/{filename}', compress_type = zipfile.ZIP_DEFLATED)
    zip_file.close()
    print("zipped")
    shutil.copy(f'/Users/roviros/Desktop/hackathon/{zip_filename}.zip',f'{filePath}/{email}')
    os.remove(f"/Users/roviros/Desktop/hackathon/{zip_filename}.zip")
    os.remove(f'{file_location}')

    return {"info": f"file '{uploaded_file.filename}' saved as '{zip_filename}.zip'"}

    #END OF ZIPPING THE FILE LOGIC

# LOGIC SHOW ALL FILES OF USER.
def show_files(email:str):
    try:
        return os.listdir(f"{filePath}/{email}")

    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail = f"Oopss...Something went wrong!")
        
# LOGIC TO SHARE FILE WITH OTHER USER BY EMAIL,.
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
    
# LOGIC TO DELETE FILE BY NAME.
# def delete_file(filename:str, email:str):
#     try:
#         delete_file_location = f"{filePath}/{email}/{filename}" #here email and the filename will come
#         os.chmod(delete_file_location, 0o777)
#         os.remove(f"{delete_file_location}")
#         return JSONResponse(status_code=status.HTTP_200_OK, content="Deleted file successfully!")
   
#     except: 
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = f"This file - '{filename}' doesn't exist in {email}'s account!")

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
    print(filename)
    filePath = "/Users/roviros/Desktop/files_uploaded_cloudwiry"

    # download_file_location = f"{filePath}/{email}/{filename}"
    # print(download_file_location)

    try:
        filePath = f"{filePath}/{email}/{filename}"
        return filePath
    
    except:
        # print(filePath)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "This file name was not found in our database!")



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


    # dir = "/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/trash"

    try:
        for files in os.listdir(empty_trash_file_location):
            path = os.path.join(empty_trash_file_location, files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)


        # os.remove(f"{filePath}")
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
    
    

