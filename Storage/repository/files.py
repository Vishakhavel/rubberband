
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



def upload_file(email:str, uploaded_file: UploadFile = File(...)):
    print(email)
    print(email[1:-1])
    email = email[1:-1]
    file_location=os.path.join(filePath, "{email}/{uploaded_file.filename}")

    #ZIPPING FILES HERE.

    zip_file_name = uploaded_file.filename.split(".")[0]
    print(zip_file_name)

    my_zip = zipfile.ZipFile()


    #END OF ZIPPING LOGIC

    # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())


        

    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}
   

def show_files(email:str):
    try:
        return os.listdir(f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}")
        # return os.listdir(os.path.join(filePath, "{email}"))

    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail = f"This file was not found in our database!")
        

def share_file(sender:str,reciever:str,filename:str):
    # try:
    print(sender)
    print(reciever[1:-1])
    print(filename)
    
    # reciever = reciever[1:-1]
    original = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{sender}/{filename}"

    # original = os.path.join(filePath, f"{sender}/{filename}")


    target = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{reciever}/{filename}"


    # target = os.path.join(filePath, f"{reciever}/{filename}")
    shutil.copyfile(original, target)

    return JSONResponse(status_code=status.HTTP_200_OK, content=f"File shared successfully to {reciever}")
    
    # except:
    #     return "jhi"

        # return {'details':"shared file successfully"}
        # print(sender)
        # print(reciever[1:-1])
        
        # reciever = reciever[1:-1]
        # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{reciever}/{uploaded_file.filename}"


        
        # return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}


    # except:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"This EMAIL ID was not found in our database!")


def delete_file(filename:str, email:str):
    try:
        filePath = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/{filename}" #here email and the filename will come
        os.chmod(filePath, 0o777)
        os.remove(f"{filePath}")
    

        # os.remove(filePath)
        return JSONResponse(status_code=status.HTTP_200_OK, content="Deleted file successfully!")
    # return {"detail":"deleted!", status_code}
    except: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = f"hmmmmm... Something went wrong.")


def rename_file(email:str,old_name:str,new_name:str):
    sourceFilePath = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/{old_name}"
    destinationFilePath = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/{new_name}"

    try:
        os.rename(sourceFilePath, destinationFilePath)
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"File {old_name} successfully renamed to {new_name}")
    # print(sourceFilePath)
    # try:
    #     return "rename successful!"
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"This file name was not found in our database!")


    # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{uploaded_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(uploaded_file.file.read())
    # return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}


def download_file(id:int, email:str, filename:str):

    filePath = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/{filename}"
    return filePath

    # return JSONResponse(status_code=status.HTTP_200_OK, content="Downloaded file successfully!")



    # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{uploaded_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(uploaded_file.file.read())
    # return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}