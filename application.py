from fastapi import FastAPI
from typing import List
from Storage import models   #This means from the same directory, import schemas.
from Storage.database import engine
from Storage.routers import authentication, file, user, authentication

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)











