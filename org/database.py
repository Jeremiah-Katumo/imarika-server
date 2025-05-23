from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Get environment variables

DATABASE_DRIVER = os.getenv("DATABASE_DRIVER")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

pymysql.install_as_MySQLdb()

SQLALCHEMY_DATABASE_URL = f'{DATABASE_DRIVER}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_session = Annotated[Session, Depends(get_db)]