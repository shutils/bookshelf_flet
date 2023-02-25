from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

engine = create_engine("sqlite:///app.db")
engine.connect()
session = Session(engine)


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]


def init_db():
    Base.metadata.create_all(engine)


def create_book(title: str) -> None:
    book = Book(
        title=title
    )
    session.add(book)
    session.commit()


def get_book_all() -> list[Book]:
    books = session.query(Book).all()
    return books


def delete_book(id: int) -> None:
    session.query(Book).filter_by(id=id).delete()
    session.commit()
