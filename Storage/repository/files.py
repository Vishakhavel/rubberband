
from pydantic import FilePath
from sqlalchemy.orm import Session
from fastapi import  status, HTTPException, File, UploadFile
from .. import schemas, models
import os
import shutil
from fastapi.responses import JSONResponse


# def get_all(db: Session):
#     files = db.query(models.File).all()
#     print(files)
#     return files

# def getFilesById(id:int,db:Session):
#     # user_id = request.user_id

#     files = db.query(models.File).filter(models.File.id==id)
#     print(files)
#     #return "hi"
#     return files


# def create(request: schemas.File, db: Session):
#     new_file = models.File(title=request.title, body = request.body, user_id = request.user_id)
#     #LOGIC TO GET THE CURRENT USER'S ID
#     #user_id = 

#     db.add(new_file)
#     db.commit()
#     db.refresh(new_file)
#     return new_file


# def destroy(id: int, db: Session):
#     file = db.query(models.File).filter(models.File.id == id)
#     if not file:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"File with ID {id} was not found in our DB")
#     file.delete(synchronize_session=False)
#     db.commit() #you've to commit after you do anything on the DB
#     return {'status': f'Deleted ID = {id} successfully'}


# def update(id:int, request:schemas.File, db:Session):
#     #print(request)
#     # This one is not working if i put request directly in the update bracket
#     file =db.query(models.File).filter(models.File.id == id)
#     if not file.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"File with ID {id} was not found in our DB")

#     file.update({'title': request.title, 'body':request.body}, synchronize_session=False)
#     db.commit()
#     return 'success'


# def get_id(id:int, db:Session):
#     file = db.query(models.File).filter(models.File.id == id).first()
#     if not file: # cannot find the entry in the database.
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'File with ID {id} is not found in our database')
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'detail' : f'File with ID {id} is not found in our database'}
#     return file


def upload_file(email:str, uploaded_file: UploadFile = File(...)):
    print(email)
    print(email[1:-1])
    email = email[1:-1]
    file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}
   

def show_files(email:str):
    try:
        return os.listdir(f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}")

    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail = f"This file was not found in our database!")
        

def share_file(sender:str,reciever:str,filename:str):
    # try:
    print(sender)
    print(reciever[1:-1])
    print(filename)
    
    # reciever = reciever[1:-1]
    original = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{sender}/{filename}"
    target = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{reciever}/{filename}"
    shutil.copyfile(original, target)
    return "done"
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
        return "rename success!"
    # print(sourceFilePath)
    # try:
    #     return "rename successful!"
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"This file name was not found in our database!")


    # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{uploaded_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(uploaded_file.file.read())
    # return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}


def download_file():
    return "download successful!"


    # file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{uploaded_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(uploaded_file.file.read())
    # return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}