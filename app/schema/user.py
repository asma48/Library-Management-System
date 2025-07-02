from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import List, Optional, Annotated, Literal
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    staff  = "staff"

class Create_User(BaseModel):
    name: str
    email: EmailStr
    password: str
        
class User_log_In(BaseModel):
    email: EmailStr
    password : str

class User_delete(BaseModel):
    email: EmailStr
    password : str


class Current_User(BaseModel):
    id: int
    role: str    
