
from starlette import status
from jose import jwt, JWTError
from ..schema.user import Current_User
from datetime import timedelta, datetime
from ..models.database_model import User
from passlib.context import CryptContext
from app.database.config import db_session
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials







SECRET_KEY = 'dr53h35hbtbt5ngbr45nrth45rth5ngr5'
ALGORITHM = 'HS256'


bcrypt_context =  CryptContext(schemes= ['bcrypt'], deprecated= 'auto')

bearer_scheme = HTTPBearer()


def authenticate_user(email: str, password:str , db:db_session):
    user = db.query(User).filter(User.email == email, User.deleted_at == None).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    if not bcrypt_context.verify(password, user.password):
        raise HTTPException(status_code=404, detail="Incorrect Password")
    return user



def create_access_token(id: int, role: str, expire_delta: timedelta):
    encode = {'sub': role , 'id': id}
    expires = expire_delta + datetime.now()
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get('sub')
        id: int = payload.get('id')
        if role is None or id is None:
            return JSONResponse(content={
            'message':"Unauthorised User","status_code":401},
                        status_code=status.HTTP_401_UNAUTHORIZED)
        return Current_User(id = id, role = role)
    except JWTError:
        return JSONResponse(content={
            'message':"Unauthorised User","status_code":401},
                    status_code=status.HTTP_401_UNAUTHORIZED)
     