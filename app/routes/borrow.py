from starlette import status
from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Depends
from ..database.config import db_session 
from fastapi.responses import JSONResponse
from ..middleware.jwt import get_current_user
from ..models.database_model import Books, Borrower, Borrower_Books, User

borrow_router = APIRouter(
    prefix = "/borrow" ,
    tags = ["Borrowing"]
)

@borrow_router.put("/borrow/{id}")
def Borrow(id: int, db: db_session, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.role in  ["user"]:    
        books_count = db.query(Borrower).filter(Borrower.user_id == current_user.id, Borrower.deleted_at == None).count()
        if books_count < 3:

            db_book = db.query(Books).filter(Books.id == id, Books.deleted_at == None).first()
            if db_book is None: 
                    return JSONResponse(content={"message": "Book does not exist" , "status_code": 404}, 
                                                                status_code=status.HTTP_404_NOT_FOUND)
            db_book.available = False
            db_book.last_borrowed_date = datetime.now()
            db.commit()
            db.refresh(db_book)
            
            db_borrow = Borrower(user_id = current_user.id, created_at = datetime.now(),)
            db.add(db_borrow)
            db.commit()
            db.refresh(db_borrow)

            db_borrowed_book = Borrower_Books(borrower_id = db_borrow.id,  book_id = id, created_at= datetime.now())
            db.add(db_borrowed_book)
            db.commit()
            db.refresh(db_borrowed_book)

            return JSONResponse(content={ "message": "Successfully Borrow", "data":{"borrow_id": db_borrow.id, "user_id" : db_borrow.user_id, "book_id": id}, 
                                    "status": 200}, status_code=status.HTTP_200_OK)

        else:
            return JSONResponse(content={ "message": "Can not Borrow more than 3 book", 
                                    "status": 406}, status_code=status.HTTP_406_NOT_ACCEPTABLE)
    else: 
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)



@borrow_router.put("/return/{id}")
def Return(id: int, db: db_session, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.role in  ["user"]:
        db_book = db.query(Books).filter(Books.id == id, Books.deleted_at == None).first()
        if db_book is None: 
            return JSONResponse(content={"message": "Book does not exist" , "status_code": 404}, 
                                                                status_code=status.HTTP_404_NOT_FOUND)
        db_book.available = True
        db.commit()
        db.refresh(db_book)

        borrow_books = db.query(Borrower).filter(Borrower.user_id == current_user.id, Borrower.deleted_at == None).all()
        for borrow in borrow_books:
            db_borrowed_book  = db.query(Borrower_Books).filter(Borrower_Books.book_id == id, Borrower_Books.deleted_by == None, Borrower_Books.borrower_id == borrow.id).first()

            if db_borrowed_book is not None:
                    db_borrowed_book.deleted_at = datetime.now()
                    db_borrowed_book.deleted_by = current_user.role
                    db.commit()
                    db.refresh(db_borrowed_book)

        return JSONResponse(content={ "message": "Successfully Return", "data":{"book_id": id}, 
                                    "status": 200}, status_code=status.HTTP_200_OK)
    else: 
        return JSONResponse(content={"message": "You don't have permission to perform this action", "status": 401}, status_code=status.HTTP_401_UNAUTHORIZED)