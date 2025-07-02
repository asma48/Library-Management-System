from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import List, Optional, Annotated, Literal
from datetime import datetime, date



class Borrow(BaseModel):

    user_id: int 
