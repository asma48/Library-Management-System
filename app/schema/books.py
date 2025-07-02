from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import List, Optional, Annotated, Literal
from datetime import datetime, date



class Create_Book(BaseModel):

    title:str 
    isbn : int
    author_id: int
    published_date: date



class Books_List(BaseModel):
    id : int
    title:str 
    isbn : int
    author_id: int
    published_date: datetime
    last_borrowed_date: datetime
    class Config:
        orm_mode = True


class Update_Book(BaseModel):
    title:str 
    isbn : int
    author_id: int
    published_date: date
    last_borrowed_date: datetime