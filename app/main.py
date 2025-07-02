from fastapi import FastAPI
from app.routes.author import author_router
from app.routes.user import user_router
from app.routes.books import book_router
from app.routes.borrow import borrow_router



app = FastAPI()

app.include_router(user_router)
app.include_router(borrow_router)
app.include_router(author_router)
app.include_router(book_router)