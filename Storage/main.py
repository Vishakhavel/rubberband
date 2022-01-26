from fastapi import FastAPI
from typing import List
from . import models   #This means from the same directory, import schemas.
from .database import engine
from .routers import authentication, file, user, authentication

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)











