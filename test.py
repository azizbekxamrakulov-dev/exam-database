"""
Library Management System test script.

Ushbu skript kutubxona tizimidagi barcha servis funksiyalarni test qiladi.
"""

from library.db import Base, engine
from library.services import (
    create_author,
    get_author_by_id,
    get_all_authors,
    update_author,
    create_book,
    get_book_by_id,
    get_all_books,
    search_books_by_title,
    create_student,
    get_student_by_id,
    get_all_students,
    update_student_grade,
    borrow_book,
    get_student_borrow_count,
    get_currently_borrowed_books,
    return_book,
    get_books_by_author,
    get_overdue_borrows,
)


def run_tests() -> None:
    """
    Barcha servis funksiyalarni test qiladi.
    """

    Base.metadata.create_all(engine)

    # author tests

    author1 = create_author("Abdulla Qodiriy", "O'zbek yozuvchisi")
    print("Author 1:", author1)

    author2 = create_author("Cho'lpon", "Shoir va yozuvchi")
    print("Author 2:", author2)

    print("Get Author 1:", get_author_by_id(author1.id))
    print("Get Author 2:", get_author_by_id(author2.id))

    print("All Authors:", get_all_authors())

    print("Update Author 1:", update_author(author1.id, name="A. Qodiriy"))
    print("Update Author 2:", update_author(author2.id, bio="Mashhur shoir"))

    # Book tests

    book1 = create_book("O'tgan kunlar", author1.id, 1926)
    print("Book 1:", book1)

    book2 = create_book("Kecha va Kunduz", author2.id, 1935)
    print("Book 2:", book2)

    print("Get Book 1:", get_book_by_id(book1.id))
    print("Get Book 2:", get_book_by_id(book2.id))

    print("All Books:", get_all_books())

    print("Search Books:", search_books_by_title("kun"))

    # Student tests

    student1 = create_student("Ali Valiyev", "ali@test.com", "2-kurs")
    print("Student 1:", student1)

    student2 = create_student("Vali Aliyev", "vali@test.com", "3-kurs")
    print("Student 2:", student2)

    print("Get Student 1:", get_student_by_id(student1.id))
    print("Get Student 2:", get_student_by_id(student2.id))

    print("All Students:", get_all_students())

    print("Update Student 1:", update_student_grade(student1.id, "4-kurs"))
    print("Update Student 2:", update_student_grade(student2.id, "1-kurs"))

    # Borrow tests

    borrow1 = borrow_book(student1.id, book1.id)
    print("Borrow 1:", borrow1)

    borrow2 = borrow_book(student2.id, book2.id)
    print("Borrow 2:", borrow2)

    print("Student1 borrow count:", get_student_borrow_count(student1.id))
    print("Student2 borrow count:", get_student_borrow_count(student2.id))

    print("Currently Borrowed:", get_currently_borrowed_books())

    # Return tests

    print("Return 1:", return_book(borrow1.id))
    print("Return 2:", return_book(borrow2.id))

    # Query tests

    print("Books by Author1:", get_books_by_author(author1.id))
    print("Books by Author2:", get_books_by_author(author2.id))

    print("Overdue Borrows:", get_overdue_borrows())


if __name__ == "__main__":
    run_tests()