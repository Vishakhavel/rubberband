from fastapi import FastAPI
from typing import List
from Storage import models  
from Storage.database import engine
from Storage.routers import authentication, file, user, authentication

# INITALIZING APP
app = FastAPI()

# LOADING DATABASE MODELS
models.Base.metadata.create_all(engine)

# ROUTERS
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)











