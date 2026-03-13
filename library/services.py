from datetime import datetime
from sqlalchemy import select

from .db import SessionLocal
from .models import Author
from .models import Book
from .models import Borrow
from .models import Student


def create_author(name: str, bio: str | None = None) -> Author | None:
    """
    Yangi muallif yaratadi.

    Agar shu nom bilan muallif mavjud bo\'lsa,
    yangi yozuv qo\'shilmaydi va mavjud muallif qaytariladi.
    """

    with SessionLocal() as session:
        stmt = select(Author).where(Author.name == name)
        existing_author = session.execute(stmt).scalars().first()

        if existing_author:
            print(f"Author '{name}' already exists.")
            return existing_author

        author = Author(name=name, bio=bio)

        session.add(author)
        session.commit()
        session.refresh(author)

        return author


def get_author_by_id(author_id: int) -> Author | None:
    """
    ID orqali muallifni topadi.

    Args:
        author_id (int): Muallif identifikatori.

    Returns:
        Author | None: Agar muallif topilsa Author obyektini,
        aks holda None qaytaradi.
    """
    with SessionLocal() as session:
        stmt = select(Author).where(Author.id == author_id)
        author = session.execute(stmt).scalar_one_or_none()
        return author


def get_all_authors() -> list[Author]:
    """
    Barcha mualliflarni qaytaradi.

    Returns:
        list[Author]: Mualliflar ro'yxati.
    """
    with SessionLocal() as session:
        stmt = select(Author)
        authors = session.execute(stmt).scalars().all()
        return authors


def update_author(
    author_id: int, name: str | None = None, bio: str | None = None
) -> Author | None:
    """
    Muallif ma'lumotlarini yangilaydi.

    Args:
        author_id (int): Muallif identifikatori.
        name (str | None): Yangi ism.
        bio (str | None): Yangi bio.

    Returns:
        Author | None: Yangilangan muallif yoki None agar topilmasa.
    """
    with SessionLocal() as session:
        stmt = select(Author).where(Author.id == author_id)
        author = session.execute(stmt).scalar_one_or_none()

        if author is None:
            return None

        if name is not None:
            author.name = name

        if bio is not None:
            author.bio = bio

        session.commit()
        session.refresh(author)

        return author


def delete_author(author_id: int) -> bool:
    """
    Muallifni o'chiradi.

    Agar muallifga tegishli kitoblar mavjud bo'lsa,
    o'chirish amalga oshirilmaydi.

    Args:
        author_id (int): Muallif identifikatori.

    Returns:
        bool: True agar muvaffaqiyatli o'chirilsa,
        False agar muallif topilmasa yoki kitoblari mavjud bo'lsa.
    """
    with SessionLocal() as session:
        stmt = select(Author).where(Author.id == author_id)
        author = session.execute(stmt).scalar_one_or_none()

        if author is None:
            return False

        if author.books:
            return False

        session.delete(author)
        session.commit()

        return True


def create_book(
    title: str, author_id: int, published_year: int, isbn: str | None = None
) -> Book | None:
    """
    Yangi kitob yaratadi.

    Agar shu nom bilan kitob mavjud bo\'lsa,
    yangi yozuv qo\'shilmaydi va mavjud kitob qaytariladi.
    """

    with SessionLocal() as session:
        stmt = select(Book).where(Book.title == title)
        existing_book = session.execute(stmt).scalars().first()

        if existing_book:
            print(f"Book '{title}' already exists.")
            return existing_book

        book = Book(
            title=title,
            author_id=author_id,
            published_year=published_year,
            isbn=isbn,
        )

        session.add(book)
        session.commit()
        session.refresh(book)

        return book


def get_book_by_id(book_id: int) -> Book | None:
    """
    ID orqali kitobni topadi.

    Args:
        book_id (int): Kitob identifikatori.

    Returns:
        Book | None: Agar kitob topilsa Book obyektini,
        aks holda None qaytaradi.
    """
    with SessionLocal() as session:
        stmt = select(Book).where(Book.id == book_id)
        book = session.execute(stmt).scalar_one_or_none()

        return book


def get_all_books() -> list[Book]:
    """
    Barcha kitoblarni qaytaradi.

    Returns:
        list[Book]: Kitoblar ro'yxati.
    """
    with SessionLocal() as session:
        stmt = select(Book)
        books = session.execute(stmt).scalars().all()

        return books


def search_books_by_title(title: str) -> list[Book]:
    """
    Kitoblarni nomi bo'yicha qidiradi (partial match).

    Args:
        title (str): Qidirilayotgan kitob nomi.

    Returns:
        list[Book]: Mos keluvchi kitoblar ro'yxati.
    """
    with SessionLocal() as session:
        stmt = select(Book).where(Book.title.ilike(f"%{title}%"))
        books = session.execute(stmt).scalars().all()

        return books


def delete_book(book_id: int) -> bool:
    """
    Kitobni o'chiradi.

    Args:
        book_id (int): Kitob identifikatori.

    Returns:
        bool: True agar muvaffaqiyatli o'chirilsa,
        False agar kitob topilmasa.
    """
    with SessionLocal() as session:
        book = session.get(Book, book_id)

        if book is None:
            return False

        session.delete(book)
        session.commit()

        return True


def create_student(
    full_name: str, email: str, grade: str | None = None
) -> Student | None:
    """
    Yangi talaba yaratadi.

    Agar shu email bilan talaba bazada mavjud bo\'lsa,
    yangi talaba qo\'shilmaydi va mavjud talaba qaytariladi.

    Args:
        full_name (str): Talabaning to\'liq ismi
        email (str): Talabaning email manzili
        grade (str | None): Talabaning kursi yoki sinfi

    Returns:
        Student | None: Yangi yaratilgan yoki mavjud talaba
    """

    with SessionLocal() as session:
        stmt = select(Student).where(Student.email == email)
        existing_student = session.execute(stmt).scalars().first()

        if existing_student:
            print(f"Student with email '{email}' already exists.")
            return existing_student

        student = Student(full_name=full_name, email=email, grade=grade)

        session.add(student)
        session.commit()
        session.refresh(student)

        return student


def get_student_by_id(student_id: int) -> Student | None:
    """
    ID orqali talabani topadi.

    Args:
        student_id (int): Talaba identifikatori.

    Returns:
        Student | None: Agar talaba topilsa Student obyektini,
        aks holda None qaytaradi.
    """
    with SessionLocal() as session:
        stmt = select(Student).where(Student.id == student_id)
        student = session.execute(stmt).scalar_one_or_none()

        return student


def get_all_students() -> list[Student]:
    """
    Barcha talabalarni qaytaradi.

    Returns:
        list[Student]: Talabalar ro'yxati.
    """
    with SessionLocal() as session:
        stmt = select(Student)
        students = session.execute(stmt).scalars().all()

        return students


def update_student_grade(student_id: int, grade: str) -> Student | None:
    """
    Talabaning kursini yangilaydi.

    Args:
        student_id (int): Talaba identifikatori.
        grade (str): Yangi kurs yoki sinf.

    Returns:
        Student | None: Yangilangan talaba obyektini,
        aks holda None qaytaradi.
    """
    with SessionLocal() as session:
        stmt = select(Student).where(Student.id == student_id)
        student = session.execute(stmt).scalar_one_or_none()

        if student is None:
            return None

        student.grade = grade

        session.commit()
        session.refresh(student)

        return student


def borrow_book(student_id: int, book_id: int) -> Borrow | None:
    """
    Talabaga kitob berish funksiyasi.
    """

    with SessionLocal() as session:
        student = session.get(Student, student_id)
        book = session.get(Book, book_id)

        if student is None or book is None:
            return None

        if not book.is_available:
            print("Book is not available.")
            return None

        stmt = select(Borrow).where(
            Borrow.student_id == student_id,
            Borrow.book_id == book_id,
            Borrow.returned_at.is_(None),
        )

        existing_borrow = session.execute(stmt).scalars().first()

        if existing_borrow:
            print("Borrow record already exists.")
            return existing_borrow

        stmt = select(Borrow).where(
            Borrow.student_id == student_id, Borrow.returned_at.is_(None)
        )

        active_borrows = session.execute(stmt).scalars().all()

        if len(active_borrows) >= 3:
            print("Student already has 3 borrowed books.")
            return None

        borrow = Borrow(student_id=student_id, book_id=book_id)

        book.is_available = False

        session.add(borrow)
        session.commit()
        session.refresh(borrow)

        return borrow


def return_book(borrow_id: int) -> bool:
    """
    Kitobni qaytarish funksiyasi.

    Args:
        borrow_id (int): Borrow identifikatori.

    Returns:
        bool: True agar muvaffaqiyatli qaytarilsa,
        False agar borrow topilmasa.
    """

    with SessionLocal() as session:
        borrow = session.get(Borrow, borrow_id)

        if borrow is None:
            return False
        if borrow.returned_at is not None:
            return False

        borrow.returned_at = datetime.utcnow()

        borrow.book.is_available = True

        session.commit()

        return True


def get_student_borrow_count(student_id: int) -> int:
    """
    Talabaning jami olgan kitoblari sonini hisoblaydi.

    Args:
        student_id (int): Talaba identifikatori.

    Returns:
        int: Talabaning jami borrow qilgan kitoblari soni.
    """

    with SessionLocal() as session:
        stmt = select(Borrow).where(Borrow.student_id == student_id)

        borrows = session.execute(stmt).scalars().all()

        return len(borrows)


def get_currently_borrowed_books() -> list[tuple[Book, Student, datetime]]:
    """
    Hozirda band bo'lgan kitoblar va ularni olgan talabalar.

    Returns:
        list[tuple[Book, Student, datetime]]:
        (Book, Student, borrowed_at) ko'rinishidagi ro'yxat.
    """

    with SessionLocal() as session:
        stmt = (
            select(Book, Student, Borrow.borrowed_at)
            .select_from(Borrow)
            .join(Book)
            .join(Student)
            .where(Borrow.returned_at.is_(None))
        )

        result = session.execute(stmt).all()

        return result


def get_books_by_author(author_id: int) -> list[Book]:
    """
    Muayyan muallifning barcha kitoblarini qaytaradi.

    Args:
        author_id (int): Muallif identifikatori.

    Returns:
        list[Book]: Muallifga tegishli kitoblar ro'yxati.
    """

    with SessionLocal() as session:
        stmt = select(Book).where(Book.author_id == author_id)

        books = session.execute(stmt).scalars().all()

        return books


def get_overdue_borrows() -> list[tuple[Borrow, Student, Book, int]]:
    """
    Qaytarish muddati o'tib ketgan kitoblarni aniqlaydi.

    Returns:
        list[tuple[Borrow, Student, Book, int]]:
        (Borrow, Student, Book, kechikkan_kunlar) ko'rinishidagi ro'yxat.
    """

    with SessionLocal() as session:
        stmt = select(Borrow).where(
            Borrow.returned_at.is_(None), Borrow.due_date < datetime.utcnow()
        )

        borrows = session.execute(stmt).scalars().all()

        result = []

        for b in borrows:
            days_late = (datetime.utcnow() - b.due_date).days
            result.append((b, b.student, b.book, days_late))

        return result