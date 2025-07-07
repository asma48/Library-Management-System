from faker import Faker
from sqlalchemy.orm import Session
from app.models.database_model import Author


fake = Faker()

def seed_author(db: Session, count: int):
    for _ in range(count):
        name = fake.unique.name()
        bio = fake.text()
        if not db.query(Author).filter(Author.name == name).first():
            author = Author(
                name=name,
                bio =bio
            )
            db.add(author)
    db.commit()
