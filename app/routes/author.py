from starlette import status
from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Depends
from ..database.config import db_session 
from ..models.database_model import Author
from fastapi.responses import JSONResponse
from ..middleware.jwt import get_current_user
from ..schema.author import Create_Author, Author_List, Author_Update


author_router = APIRouter()

@author_router.post("/create")
def new_author(author:Create_Author, db: db_session, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.role in  ["admin" , "staff"]:
        db_author = db.query(Author).filter(Author.name == author.name, Author.bio == author.bio, Author.deleted_at == None).first()
        if db_author is not None:
            return JSONResponse(content={"message": "author already existed", "status": 406}, status_code=status.HTTP_406_NOT_ACCEPTABLE)
        
        db_create_author = Author(name = author.name, bio = author.bio, create_at = datetime.now())
        db.add(db_create_author)
        db.commit()
        db.refresh(db_create_author) 
        return JSONResponse(content={
                        "message": "Author Added Successfully",
                        "data": {"id": db_create_author.id,"name": db_create_author.name, 
                        "bio" : db_create_author.bio}, 
                        "status":200},
                        status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)


@author_router.get("/list_of_authors")
def list_of_authors(db:db_session , current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.role in  ["admin" , "staff"]:
        db_authors = db.query(Author).filter(Author.deleted_at == None).all()
        author_list = []
        for author in db_authors:
            author_list.append(author)

        return  author_list

    else: 
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)


@author_router.get("/{author_id}")
def author(author_id: int ,db:db_session, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.role in  ["admin" , "staff"]:
        db_author = db.query(Author).filter(Author.id == author_id, Author.deleted_at == None).first()
        if db_author is None:
            return JSONResponse(content={"message": "Author does not exist" , "status_code": 404}, 
                                                            status_code=status.HTTP_404_NOT_FOUND)
        
        return JSONResponse(content={ "message": "Author", "data":{"id": db_author.id, "name" : db_author.name, "bio" : db_author.bio}, 
                                    "status": 200}, status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)



@author_router.put("/update/{author_id}")
def update_author(author_id: int, author: Author_Update , db:db_session, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.role in  ["admin" , "staff"]:
        db_author = db.query(Author).filter(Author.id == author_id, Author.deleted_at == None).first()
        if author != db_author:
            db_author.name = author.name
            db_author.bio = author.bio
            db_author.updated_at = datetime.now()
        db.commit()
        db.refresh(db_author)
        return JSONResponse(content={"message":"Successfully Updated", "data": {"id": db_author.id, "name" : db_author.name, "bio" : db_author.bio}, 
                            "status" : 200}, status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)


@author_router.delete("/delete/{author_id}")
def delete_author(author_id: int, db:db_session , current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.role in  ["admin" , "staff"]:
        db_author = db.query(Author).filter(Author.id == author_id, Author.deleted_at == None).first()
        if db_author is None:
            return JSONResponse(content={"message": "Author Does Not Exist", "status" : 404}, status_code=status.HTTP_404_NOT_FOUND) 
        db_author.deleted_at = datetime.now()
        db_author.deleted_by = current_user.role
        db.commit()
        db.refresh(db_author) 
        return JSONResponse(content={"message": "Author Deleted Successfully", "status" : 200}, status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)

