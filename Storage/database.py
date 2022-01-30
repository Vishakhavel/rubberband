from click import password_option
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from dotenv import load_dotenv

load_dotenv()

user = os.environ["DB_USER"]
password = os.environ["DB_PASS"]
host = os.environ["DB_HOST"]
port = os.environ["DB_PORT"]
database = os.environ["DB_NAME"]

# BUILDING DB CONNECTION URL.
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

# UNCOMMENT THE LINE BELOW TO USE SQLITE INSTEAD OF PRODUCTION DB.
# SQLALCHEMY_DATABASE_URL = "sqlite:///./storage.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()