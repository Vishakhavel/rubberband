
from sqlalchemy.orm import Session
from fastapi import  status, HTTPException, File, UploadFile
from .. import schemas, models
import os

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


def upload(email:str, uploaded_file: UploadFile = File(...)):
    print(email)
    file_location = f"/Users/roviros/Desktop/files_uploaded_cloudwiry/{email}/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}
    return file.upload_file()

def show_files():
    try:
        return os.listdir("/Users/roviros/Desktop/files_uploaded_cloudwiry/")

    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail = f"This file was not found in our database!")
        

def share(uploaded_file: UploadFile = File(...)):
    try:
        return {'details':"shared file successfully"}

    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"This EMAIL ID was not found in our database!")

    


def delete_file():
    try:
        os.remove("/Users/roviros/Desktop/files_uploaded_cloudwiry/") 
        return "deleted!"
    except: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"This EMAIL ID was not found in our database!")


def rename_file():
    try:
        return "rename successful!"
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