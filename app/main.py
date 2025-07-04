from fastapi import FastAPI
from app.routes.author import author_router
from app.routes.user import user_router
from app.routes.books import book_router
from app.routes.borrow import borrow_router



app = FastAPI(title="Library Management System")

app.include_router(user_router, prefix= "/user", tags=["User"])
app.include_router(borrow_router, prefix = "/borrow" ,tags = ["Borrowing"])
app.include_router(author_router, tags= ["Author"] , prefix= "/author")
app.include_router(book_router, prefix = "/books" ,tags = ["Books"])