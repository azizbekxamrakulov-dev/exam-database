from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from .db import SessionLocal
from .models import Author, Book, Student, Borrow


# ---------------- AUTHOR CRUD ----------------

def create_author(name: str, bio: str | None = None):
    with SessionLocal() as db:
        author = Author(name=name, bio=bio)
        db.add(author)
        db.commit()
        db.refresh(author)
        return author


def get_author_by_id(author_id: int):
    with SessionLocal() as db:
        return db.get(Author, author_id)


def get_all_authors():
    with SessionLocal() as db:
        return db.scalars(select(Author)).all()


def update_author(author_id: int, name=None, bio=None):
    with SessionLocal() as db:
        author = db.get(Author, author_id)

        if not author:
            return None

        if name:
            author.name = name

        if bio:
            author.bio = bio

        db.commit()
        db.refresh(author)

        return author


def delete_author(author_id: int):
    with SessionLocal() as db:
        author = db.get(Author, author_id)

        if not author:
            return False

        if author.books:
            return False

        db.delete(author)
        db.commit()

        return True


# ---------------- BOOK CRUD ----------------

def create_book(title, author_id, published_year, isbn=None):

    with SessionLocal() as db:
        book = Book(
            title=title,
            author_id=author_id,
            published_year=published_year,
            isbn=isbn
        )

        try:
            db.add(book)
            db.commit()
            db.refresh(book)
            return book

        except IntegrityError:
            db.rollback()
            return None


def get_book_by_id(book_id):
    with SessionLocal() as db:
        return db.get(Book, book_id)


def get_all_books():
    with SessionLocal() as db:
        return db.scalars(select(Book)).all()


def search_books_by_title(title):

    with SessionLocal() as db:
        stmt = select(Book).where(Book.title.ilike(f"%{title}%"))
        return db.scalars(stmt).all()


def delete_book(book_id):

    with SessionLocal() as db:

        book = db.get(Book, book_id)

        if not book:
            return False

        db.delete(book)
        db.commit()

        return True


# ---------------- STUDENT CRUD ----------------

def create_student(full_name, email, grade=None):

    with SessionLocal() as db:

        student = Student(
            full_name=full_name,
            email=email,
            grade=grade
        )

        try:
            db.add(student)
            db.commit()
            db.refresh(student)
            return student

        except IntegrityError:
            db.rollback()
            return None


def get_student_by_id(student_id):

    with SessionLocal() as db:
        return db.get(Student, student_id)


def get_all_students():

    with SessionLocal() as db:
        return db.scalars(select(Student)).all()


def update_student_grade(student_id, grade):

    with SessionLocal() as db:

        student = db.get(Student, student_id)

        if not student:
            return None

        student.grade = grade

        db.commit()
        db.refresh(student)

        return student


# ---------------- BORROW LOGIC ----------------

def borrow_book(student_id, book_id):

    with SessionLocal() as db:

        student = db.get(Student, student_id)
        book = db.get(Book, book_id)

        if not student or not book:
            return None

        if not book.is_available:
            return None

        active_borrows = db.scalar(
            select(func.count())
            .select_from(Borrow)
            .where(
                Borrow.student_id == student_id,
                Borrow.returned_at == None
            )
        )

        if active_borrows >= 3:
            return None

        borrow = Borrow(
            student_id=student_id,
            book_id=book_id,
            borrowed_at=datetime.utcnow(),
            due_date=datetime.utcnow() + timedelta(days=14)
        )

        book.is_available = False

        db.add(borrow)
        db.commit()
        db.refresh(borrow)

        return borrow


def return_book(borrow_id):

    with SessionLocal() as db:

        borrow = db.get(Borrow, borrow_id)

        if not borrow or borrow.returned_at:
            return False

        borrow.returned_at = datetime.utcnow()

        borrow.book.is_available = True

        db.commit()

        return True


# ---------------- EXTRA QUERIES ----------------

def get_student_borrow_count(student_id):

    with SessionLocal() as db:

        return db.scalar(
            select(func.count())
            .select_from(Borrow)
            .where(Borrow.student_id == student_id)
        )


def get_currently_borrowed_books():

    with SessionLocal() as db:

        stmt = (
            select(Book, Student, Borrow.borrowed_at)
            .join(Borrow)
            .join(Student)
            .where(Borrow.returned_at == None)
        )

        return db.execute(stmt).all()


def get_books_by_author(author_id):

    with SessionLocal() as db:

        stmt = select(Book).where(Book.author_id == author_id)

        return db.scalars(stmt).all()


def get_overdue_borrows():

    with SessionLocal() as db:

        now = datetime.utcnow()

        stmt = (
            select(Borrow, Student, Book)
            .join(Student)
            .join(Book)
            .where(
                Borrow.returned_at == None,
                Borrow.due_date < now
            )
        )

        results = []

        for borrow, student, book in db.execute(stmt).all():

            days_late = (now - borrow.due_date).days

            results.append((borrow, student, book, days_late))

        return results