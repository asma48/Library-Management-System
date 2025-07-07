import random
from faker import Faker
from sqlalchemy.orm import Session
from app.models.database_model import Author, Books


fake = Faker()


def seed_book(db: Session, count: int):
    for _ in range(count):
        author_ids = [author.id for author in db.query(Author).all()]
        title = fake.unique.sentence(nb_words=4)
        isbn = fake.isbn13()
        author_id = random.choice(author_ids)
        published_date = fake.date()
    
        if not db.query(Books).filter(Books.title == title).first():
            books = Books(
                title =title,
                isbn = isbn,
                author_id = author_id,
                published_date = published_date
            )
            db.add(books)
    db.commit()

