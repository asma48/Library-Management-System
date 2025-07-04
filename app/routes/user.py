from typing import Annotated
from starlette import status
from pydantic import EmailStr
from fastapi import APIRouter, Depends
from ..database.config import db_session
from ..models.database_model import User
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from ..middleware.jwt import bcrypt_context
from ..schema.user import Create_User, User_log_In, User_delete, UserRole
from ..middleware.jwt import get_current_user, create_access_token, authenticate_user


user_router = APIRouter(


)

@user_router.post("/sign_up")
def sign_up(role:UserRole ,user: Create_User , db:db_session):
    db_user = db.query(User).filter(User.email == user.email, User.deleted_at == None).first()
    if db_user is not None:
        return JSONResponse(content={
                    "message": "User Already Existed", 
                    "status":406},
                    status_code=status.HTTP_406_NOT_ACCEPTABLE)
    create_user = User(
        name = user.name,
        email = user.email,
        password = bcrypt_context.hash(user.password),
        role = role, 
        create_at = datetime.now()
    )
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return JSONResponse(content={
                    "message": "User Account Created Successfully",
                    "data": {"id": create_user.id, "name": create_user.name, "email": create_user.email, "role": str(create_user.role)}, 
                    "status":200},
                    status_code=status.HTTP_200_OK)


@user_router.post("/log_in")
def log_In(user: User_log_In, db: db_session):

    user = authenticate_user(user.email, user.password, db)
    if not user: 
        return JSONResponse(content={
                    "message": "User Does not exist", 
                    "status": 404},
                    status_code=status.HTTP_404_NOT_FOUND)
    token = create_access_token(user.id , user.role.value, timedelta(minutes=50))

    return JSONResponse(content={
        'message':"login succefully","status_code":200,
        "access_token":token,
        "data":{"id" :user.id,  "email":user.email}},
                            status_code=status.HTTP_200_OK)

#@user_router.put("/update_user")
#def update_user(user:, db:db_session, current_user: Annotated[dict, Depends(get_current_user)])


@user_router.delete("/delete_user")
def delet_user(user: User_delete, db:db_session, current_user: Annotated[dict, Depends(get_current_user)]):
    delete_user = authenticate_user(user.email, user.password, db)
    if delete_user.id == current_user.id or current_user.role == "admin":    
        db_user = db.query(User).filter(User.id == delete_user.id, User.deleted_at == None).first()
        db_user.deleted_at = datetime.now()
        db_user.deleted_by = current_user.role
        db.commit()
        db.refresh(db_user) 
        return JSONResponse(content={
        'message':"User Deleted Succefully","status_code":200,
        "data":{"id" :user.id,  "email":user.email}},
                            status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)

