from library.db import Base, engine
from library.services import *

Base.metadata.create_all(engine)

author = create_author("J.K Rowling")
print(author)

book = create_book("Harry Potter", author.id, 1997)
print(book)

student = create_student("Ali Valiyev", "ali@example.com")
print(student)

borrow = borrow_book(student.id, book.id)
print(borrow)

print(get_currently_borrowed_books())

return_book(borrow.id)