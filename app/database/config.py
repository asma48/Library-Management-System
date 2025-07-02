from fastapi import Depends
from typing import List, Annotated
from sqlalchemy import create_engine
from app.models.database_model import Base
from sqlalchemy.orm import sessionmaker, Session


DATABASE_URL = 'postgresql://postgres:asma12@localhost:5432/Library'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
 
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_session = Annotated[Session, Depends(get_db)]
