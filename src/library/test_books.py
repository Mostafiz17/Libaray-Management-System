from .services.book_service import (
    get_all_books,
    get_book,
    add_book,
    delete_book
)


print("All books:")
print(get_all_books())

print("\nAdding book:")
book = add_book("Clean Code", "Robert C. Martin")
print(book)

print("\nGetting book:")
print(get_book(book["id"]))

print("\nAll books:")
print(get_all_books())