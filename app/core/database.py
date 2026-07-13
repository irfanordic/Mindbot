from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

DATABASE_URL = os.getenv("DB_LINK")

engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine )
Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
        
    finally:
        db.close()    
