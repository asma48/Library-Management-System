from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import List, Optional, Annotated, Literal
from datetime import datetime




class Create_Author(BaseModel):
    name : str
    bio : str


class Author_List(BaseModel):
    id : int
    name : str
    bio : str

    class Config:
        orm_mode = True



class Author_Update(BaseModel):
    name : Optional[str]
    bio : Optional[str]