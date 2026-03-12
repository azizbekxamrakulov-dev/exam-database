from sqlalchemy import select
from datetime import datetime, timedelta
from .db import SessionLocal
from .models import Author, Book, Student, Borrow


# ======================
# AUTHOR CRUD
# ======================

def create_author(name: str, bio: str = None):
    session = SessionLocal()
    author = Author(name=name, bio=bio)
    session.add(author)
    session.commit()
    session.refresh(author)
    session.close()
    return author


def get_author_by_id(author_id: int):
    session = SessionLocal()
    author = session.get(Author, author_id)
    session.close()
    return author


def get_all_authors():
    session = SessionLocal()
    authors = session.execute(select(Author)).scalars().all()
    session.close()
    return authors


def update_author(author_id: int, name=None, bio=None):
    session = SessionLocal()
    author = session.get(Author, author_id)

    if not author:
        return None

    if name:
        author.name = name
    if bio:
        author.bio = bio

    session.commit()
    session.close()
    return author


def delete_author(author_id: int):
    session = SessionLocal()
    author = session.get(Author, author_id)

    if not author:
        return False

    if author.books:
        return False

    session.delete(author)
    session.commit()
    session.close()

    return True


# ======================
# BOOK CRUD
# ======================

def create_book(title, author_id, published_year, isbn=None):
    session = SessionLocal()

    book = Book(
        title=title,
        author_id=author_id,
        published_year=published_year,
        isbn=isbn
    )

    session.add(book)
    session.commit()
    session.refresh(book)
    session.close()

    return book


def get_book_by_id(book_id: int):
    session = SessionLocal()
    book = session.get(Book, book_id)
    session.close()
    return book


def get_all_books():
    session = SessionLocal()
    books = session.execute(select(Book)).scalars().all()
    session.close()
    return books


def search_books_by_title(title: str):
    session = SessionLocal()

    books = session.query(Book).filter(Book.title.ilike(f"%{title}%")).all()

    session.close()
    return books


def delete_book(book_id: int):
    session = SessionLocal()
    book = session.get(Book, book_id)

    if not book:
        return False

    session.delete(book)
    session.commit()
    session.close()

    return True


# ======================
# STUDENT CRUD
# ======================

def create_student(full_name, email, grade=None):
    session = SessionLocal()

    student = Student(
        full_name=full_name,
        email=email,
        grade=grade
    )

    session.add(student)
    session.commit()
    session.refresh(student)
    session.close()

    return student


def get_student_by_id(student_id):
    session = SessionLocal()
    student = session.get(Student, student_id)
    session.close()
    return student


def get_all_students():
    session = SessionLocal()
    students = session.execute(select(Student)).scalars().all()
    session.close()
    return students


def update_student_grade(student_id, grade):
    session = SessionLocal()
    student = session.get(Student, student_id)

    if not student:
        return None

    student.grade = grade
    session.commit()
    session.close()

    return student


# ======================
# BORROW LOGIC
# ======================

def borrow_book(student_id, book_id):
    session = SessionLocal()

    student = session.get(Student, student_id)
    book = session.get(Book, book_id)

    if not student or not book:
        return None

    if not book.is_available:
        return None

    active_borrows = session.query(Borrow).filter(
        Borrow.student_id == student_id,
        Borrow.returned_at == None
    ).count()

    if active_borrows >= 3:
        return None

    borrow = Borrow(
        student_id=student_id,
        book_id=book_id,
        borrowed_at=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14)
    )

    book.is_available = False

    session.add(borrow)
    session.commit()
    session.refresh(borrow)
    session.close()

    return borrow


def return_book(borrow_id):
    session = SessionLocal()

    borrow = session.get(Borrow, borrow_id)

    if not borrow or borrow.returned_at:
        return False

    borrow.returned_at = datetime.utcnow()
    borrow.book.is_available = True

    session.commit()
    session.close()

    return True


# ======================
# QUERIES
# ======================

def get_student_borrow_count(student_id):
    session = SessionLocal()

    count = session.query(Borrow).filter(
        Borrow.student_id == student_id
    ).count()

    session.close()

    return count


def get_books_by_author(author_id):
    session = SessionLocal()

    books = session.query(Book).filter(
        Book.author_id == author_id
    ).all()

    session.close()
    return books


def get_currently_borrowed_books():
    session = SessionLocal()

    results = session.query(Book, Student, Borrow.borrowed_at).join(
        Borrow, Borrow.book_id == Book.id
    ).join(
        Student, Student.id == Borrow.student_id
    ).filter(
        Borrow.returned_at == None
    ).all()

    session.close()

    return results


def get_overdue_borrows():
    session = SessionLocal()

    now = datetime.utcnow()

    borrows = session.query(Borrow, Student, Book).join(
        Student
    ).join(
        Book
    ).filter(
        Borrow.returned_at == None,
        Borrow.due_date < now
    ).all()

    result = []

    for borrow, student, book in borrows:
        days = (now - borrow.due_date).days
        result.append((borrow, student, book, days))

    session.close()

    return result