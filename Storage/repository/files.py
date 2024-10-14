from pydantic import FilePath
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, File, UploadFile, APIRouter
from fastapi.responses import JSONResponse, FileResponse
import os
import shutil
import zipfile
from dotenv import load_dotenv

# READING FROM ENV VARS
load_dotenv()  
filePath = os.getenv("BASE_FILE_DIR")
current_file_path = os.getenv("CURRENT_FILE_PATH")

router = APIRouter()

# LOGIC TO UPLOAD FILE
@router.post("/upload-file")
def upload_file(email: str, uploaded_file: UploadFile = File(...)):
    email = email.strip('"')  # remove surrounding quotes if present
    file_location = os.path.join(filePath, f"{email}/{uploaded_file.filename}")
    
    try:
        os.makedirs(os.path.dirname(file_location), exist_ok=True)  # ensure directory exists
        with open(file_location, "wb") as file_object:
            file_object.write(uploaded_file.file.read())
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            "message": f"File '{uploaded_file.filename}' successfully uploaded to '{email}'"
        })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"File upload failed: {str(e)}")


# LOGIC TO ZIP AND UPLOAD FILE
@router.post("/upload-zip-file")
def upload_and_zip_file(email: str, uploaded_file: UploadFile = File(...)):
    email = email.strip('"')
    filename = uploaded_file.filename
    zip_filename = os.path.splitext(filename)[0]  # get filename without extension
    file_location = os.path.join(filePath, f"{email}/{filename}")
    
    try:
        os.makedirs(os.path.dirname(file_location), exist_ok=True)  # ensure directory exists
        with open(file_location, "wb") as file_object:
            file_object.write(uploaded_file.file.read())

        zip_file_path = os.path.join(current_file_path, f'{zip_filename}.zip')
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            zip_file.write(file_location, arcname=filename, compress_type=zipfile.ZIP_DEFLATED)

        shutil.copy(zip_file_path, os.path.join(filePath, f"{email}/{zip_filename}.zip"))
        os.remove(zip_file_path)  # clean up the zip from the temp location
        os.remove(file_location)  # clean up the original uploaded file

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            "message": f"File '{filename}' saved as '{zip_filename}.zip'"
        })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Zipping failed: {str(e)}")


# LOGIC TO SHOW ALL FILES OF USER
@router.get("/files/{email}")
def show_files(email: str):
    try:
        files = os.listdir(f"{filePath}/{email}")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"files": files})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error listing files: {str(e)}")


# LOGIC TO SHARE FILE WITH OTHER USER
@router.post("/share-file")
def share_file(sender: str, receiver: str, filename: str):
    sender = sender.strip('"')
    receiver = receiver.strip('"')

    original = os.path.join(filePath, f"{sender}/{filename}")
    target = os.path.join(filePath, f"{receiver}/{filename}")
    
    try:
        shutil.copyfile(original, target)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": f"File '{filename}' shared successfully with '{receiver}'"
        })
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File '{filename}' not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"File sharing failed: {str(e)}")


# LOGIC TO RENAME FILE
@router.put("/rename-file")
def rename_file(email: str, old_name: str, new_name: str):
    source_file = os.path.join(filePath, f"{email}/{old_name}")
    destination_file = os.path.join(filePath, f"{email}/{new_name}")

    try:
        os.rename(source_file, destination_file)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": f"File '{old_name}' successfully renamed to '{new_name}'"
        })
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File '{old_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Renaming failed: {str(e)}")


# LOGIC TO DOWNLOAD FILE
@router.get("/download-file/{email}/{filename}")
def download_file(email: str, filename: str):
    file_location = os.path.join(filePath, f"{email}/{filename}")

    if os.path.exists(file_location):
        return FileResponse(path=file_location, filename=filename, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File '{filename}' not found")


# LOGIC TO MOVE FILE TO TRASH
@router.delete("/move-to-trash")
def move_to_trash(filename: str, email: str):
    original = os.path.join(filePath, f"{email}/{filename}")
    trash_dir = os.path.join(filePath, f"{email}_trash")
    os.makedirs(trash_dir, exist_ok=True)
    target = os.path.join(trash_dir, filename)

    try:
        shutil.move(original, target)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": f"File '{filename}' moved to trash"
        })
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File '{filename}' not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error moving file to trash: {str(e)}")


# LOGIC TO EMPTY USER'S TRASH
@router.delete("/empty-trash/{email}")
def empty_trash(email: str):
    trash_dir = os.path.join(filePath, f"{email}_trash")

    try:
        if os.path.exists(trash_dir):
            shutil.rmtree(trash_dir)
            os.makedirs(trash_dir)  # recreate the empty trash folder
            return JSONResponse(status_code=status.HTTP_200_OK, content="Trash emptied successfully")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trash directory not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error emptying trash: {str(e)}")


# LOGIC TO VIEW USER'S TRASH
@router.get("/view-trash/{email}")
def view_trash(email: str):
    trash_dir = os.path.join(filePath, f"{email}_trash")

    try:
        if os.path.exists(trash_dir):
            files = os.listdir(trash_dir)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"trash_files": files})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trash directory not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error viewing trash: {str(e)}")


# LOGIC TO RECOVER FILE FROM TRASH
@router.put("/recover-file")
def recover_file_from_trash(filename: str, email: str):
    original = os.path.join(filePath, f"{email}_trash/{filename}")
    target = os.path.join(filePath, f"{email}/{filename}")

    try:
        shutil.move(original, target)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": f"File '{filename}' recovered from trash"
        })
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File '{filename}' not found in trash")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error recovering file: {str(e)}")
