import enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, func, ForeignKey, Table , Enum , Date


Base = declarative_base()

class Borrower_Books(Base):
    
    __tablename__ ='borrower_book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    borrower_id= Column(Integer, ForeignKey('borrower.id'), index = True, nullable=True)
    book_id= Column(Integer, ForeignKey('books.id') ,index = True, nullable=True)
    create_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by =Column(String, nullable=True)

    books = relationship("Books", back_populates="borrowers")
    borrowers = relationship("Borrower", back_populates="books")


class UserRole(enum.Enum):
    admin = "admin"
    staff = "staff"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index= True)
    name = Column(String, index= True, nullable=True)
    email =Column(String, unique=True, index=True, nullable=True)
    password = Column(String, index=True, nullable=True)
    role = Column(Enum(UserRole), index=True, nullable=True)
    create_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(String, nullable=True)

    borrowers = relationship("Borrower", back_populates="users")
      

class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index= True, nullable=True)
    bio = Column(Text, index=True, nullable=True)
    create_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(String, nullable=True)

    books = relationship("Books", back_populates="author")


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index = True)
    title =  Column(String, index=True, nullable=True)
    isbn = Column(String, unique=True, index = True, nullable=True)
    author_id = Column(Integer, ForeignKey(Author.id), index = True, nullable=True)
    published_date = Column(Date, index= True, nullable=True)
    available =Column(Boolean, default=True, nullable=True)
    last_borrowed_date = Column(DateTime, index=True, nullable=True)
    create_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(String, nullable=True)
    borrowers = relationship("Borrower_Books", back_populates="books")
    author = relationship("Author", back_populates="books")



class Borrower(Base):
    __tablename__ = "borrower"

    id = Column( Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey(User.id), nullable=True)
    create_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(String, nullable=True)
    
    books = relationship("Borrower_Books", back_populates="borrowers")
    users = relationship("User", back_populates="borrowers")
    








