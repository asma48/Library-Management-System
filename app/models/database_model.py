import enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, func, ForeignKey, Table , Enum , Date


Base = declarative_base()

class Borrower_Books(Base):
    
    __tablename__ ='borrower_book'

    id = Column(Integer, primary_key=True)
    borrower_id= Column(Integer, ForeignKey('borrower.id'), index = True)
    book_id= Column(Integer, ForeignKey('books.id') ,index = True)
    create_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    deleted_by =Column(String)

    books = relationship("Books", back_populates="borrowers")
    borrowers = relationship("Borrower", back_populates="books")


class UserRole(enum.Enum):
    admin = "admin"
    staff = "staff"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index= True)
    name = Column(String, index= True)
    email =Column(String, unique=True, index=True)
    password = Column(String, index=True)
    role = Column(Enum(UserRole), index=True)
    create_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    deleted_by = Column(String)

    borrowers = relationship("Borrower", back_populates="users")
  

    

class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index= True)
    bio = Column(Text, index=True, nullable=True)
    create_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    deleted_by = Column(String)

    books = relationship("Books", back_populates="author")


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index = True)
    title =  Column(String, index=True)
    isbn = Column(String, unique=True, index = True)
    author_id = Column(Integer, ForeignKey(Author.id), index = True)
    published_date = Column(Date, index= True)
    available =Column(Boolean, default=True)
    last_borrowed_date = Column(DateTime, index=True)
    create_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    deleted_by = Column(String)
    borrowers = relationship("Borrower_Books", back_populates="books")
    author = relationship("Author", back_populates="books")



class Borrower(Base):
    __tablename__ = "borrower"

    id = Column( Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey(User.id))
    create_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    deleted_by = Column(String)
    books = relationship("Borrower_Books", back_populates="borrowers")
    users = relationship("User", back_populates="borrowers")
    








