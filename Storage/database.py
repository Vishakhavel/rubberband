from click import password_option
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#new stuff
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
#end of new stuff



#new stuff

# user = os.environ["DB_USER"]
# password = os.environ["DB_PASS"]
# host = os.environ["DB_HOST"]
# port = os.environ["DB_PORT"]
# database = os.environ["DB_NAME"]


user = "vishakhavel"
password = "vishakhavel123"
host = "cloudwirydb.cjcritax3n0n.ap-south-1.rds.amazonaws.com"
port = 5432
database = "cloudwiryDB"

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
# SQLALCHEMY_DATABASE_URL = "cloudwirydb.cjcritax3n0n.ap-south-1.rds.amazonaws.com"


#end of new stuff



# SQLALCHEMY_DATABASE_URL = "sqlite:///./storage.db"




#old stuff

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )


#old stuff ends

#new stuff

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#new stuff ends

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()