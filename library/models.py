from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base



class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    books = relationship("Book", back_populates="author")



class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    published_year: Mapped[int]
    isbn: Mapped[str | None] = mapped_column(String(13), unique=True)

    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    author = relationship("Author", back_populates="books")
    borrows = relationship("Borrow", back_populates="book")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)

    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    grade: Mapped[str | None] = mapped_column(String(20))

    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    borrows = relationship("Borrow", back_populates="student")


class Borrow(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    borrowed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    due_date: Mapped[datetime]

    returned_at: Mapped[datetime | None] = mapped_column(nullable=True)

    student = relationship("Student", back_populates="borrows")
    book = relationship("Book", back_populates="borrows")