from starlette import status
from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Depends
from ..database.config import db_session 
from ..models.database_model import Books
from fastapi.responses import JSONResponse
from ..middleware.jwt import get_current_user
from ..schema.books import Create_Book, Books_List, Update_Book



book_router = APIRouter(
    prefix = "/books" ,
    tags = ["Books"]
)


@book_router.post("/create")
def new_book(book:Create_Book, db: db_session, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.role in  ["admin", "staff"]:
        db_book = db.query(Books).filter(Books.name == book.name, Books.deleted_at == None).first()
        if db_book is not None:
            return JSONResponse(content={"message": "Book already exist", "status": 406}, status_code=status.HTTP_406_NOT_ACCEPTABLE)
        
        db_create_book = Books(title = book.title, isbn = book.isbn, 
                               author_id = book.author_id, published_date = book.published_date, 
                               available = True, created_at = datetime.now())
        db.add(db_create_book)
        db.commit()
        db.refresh(db_create_book) 
        return JSONResponse(content={
                        "message": "Book Added Successfully",
                        "data": {"id": db_create_book.id,"title": db_create_book.title, 
                        "isbn" : db_create_book.isbn}, 
                        "status":200},
                        status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)


@book_router.get("/list_of_books")
def list_of_books(db:db_session , current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.role in  ["admin" , "staff"]:
        db_books = db.query(Books).filter(Books.deleted_at == None).all()
        books_list = [Books_List.model_validate(books).model_dump() for books in db_books]
        return JSONResponse(
            content={
                "message": "List of Author",
                "data": Books_List
            }, 
            status_code=status.HTTP_200_OK
        )
    else: 
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)


@book_router.get("/{book_id}")
def author(book_id: int, db:db_session, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.role in  ["admin" , "staff"]:
        db_book = db.query(Books).filter(Books.id == book_id, Books.deleted_at == None).first()
        if db_book is None:
            return JSONResponse(content={"message": "Book does not exist" , "status_code": 404}, 
                                                            status_code=status.HTTP_404_NOT_FOUND)
        
        return JSONResponse(content={ "message": "Book", "data":{"id": db_book.id, "title": db_book.title, 
                                                                "isbn": db_book.isbn, "author_id": db_book.author_id, 
                                                                "publish_date": db_book.published_date}, 
                                    "status": 200}, status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)

@book_router.put("/update/{id}")
def update_book(id:int, book: Update_Book, db:db_session, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.role in  ["admin" ,"staff"]:
        db_book = db.query(Books).filter(Books.id == id, Books.deleted_at == None).first()    
        if book != db_book:
            db_book.title = book.title
            db_book.isbn = book.isbn
            db_book.author_id = book.author_id
            db_book.published_date = book.published_date
            db_book.updated_at = datetime.now()
        db.commit()
        db.refresh(db_book)
        updated_book = Books_List.model_validate(db_book).model_dump()

        return JSONResponse(content={"message":"Successfully Updated", "data": updated_book, 
                            "status" : 200}, status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)





@book_router.delete("/delete/{book_id}")
def delete_book(id: int, db:db_session , current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.role in  ["admin" , "staff"]:
        db_book = db.query(Books).filter(Books.id == id, Books.deleted_at == None).first()
        if db_book is None:
            return JSONResponse(content={"message": "Book Does Not Exist", "status" : 404}, status_code=status.HTTP_404_NOT_FOUND)       
        db_book.deleted_at = datetime.now()
        db_book.deleted_by = current_user.role
        db.commit()
        db.refresh(db_book)
        return JSONResponse(content={"message": "Book Deleted Successfully", "status" : 200}, status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)
