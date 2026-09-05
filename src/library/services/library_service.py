from ..models.book import EBook, PrintedBook, Returnable
from ..utils.validators import get_int
class Library:

    def __init__(self):
        self.books = []

    def add_book(self):

        # Get unique ID
        while True:
            given_id = get_int()

            id_exists = False

            for book in self.books:
                if book.id == given_id:
                    id_exists = True
                    break

            if id_exists:
                print("This ID already exists. Please enter a new ID.")
                continue

            break

        # Basic information
        title = input("Give a Book Title: ").strip()
        author = input("Give an Author Name: ").strip()

        # Book type
        while True:
            try:
                book_type = int(
                    input(
                        "\nWhich type of book do you want?\n"
                        "1. Printed Book\n"
                        "2. EBook\n"
                        "Enter choice: "
                    )
                )

                if not 1 <= book_type <= 2:
                    print("Invalid option. Please choose 1 or 2.")
                    continue

                break

            except ValueError:
                print("Please enter a number.")

        # Create the appropriate object
        if book_type == 1:

            shelf_number = input("Shelf Number: ").strip()

            copy_number = 1

            for book in self.books:
                if (
                    isinstance(book, PrintedBook)
                    and book.title.lower() == title.lower()
                    and book.author.lower() == author.lower()
                ):
                    copy_number += 1

            new_book = PrintedBook(
                given_id,
                title,
                author,
                shelf_number,
                copy_number
            )

        else:

            file_size = input("File Size: ").strip()

            new_book = EBook(
                given_id,
                title,
                author,
                file_size
            )

        # Store object
        self.books.append(new_book)

        print("\nThe book was successfully added.")
        print(new_book)

    def view_available_books(self):

        total_books = len(self.books)

        available_books = 0
        borrowed_books = 0

        print("\n========== LIBRARY BOOKS ==========")

        for book in self.books:

            if book.is_available():
                available_books += 1
            else:
                borrowed_books += 1

            print(book)
            print("-----------------------------------")

        print(f"Total copies: {total_books}")
        print(f"Available copies: {available_books}")
        print(f"Borrowed copies: {borrowed_books}")

    def search_book(self):

        search_term = input(
            "Search for a book: "
        ).strip().lower()

        found = False

        for book in self.books:

            if (
                search_term in str(book.id)
                or search_term in book.title.lower()
                or search_term in book.author.lower()
            ):

                found = True

                print("\nBook Found")
                print(f"ID: {book.id}")
                print(f"Title: {book.title}")
                print(f"Author: {book.author}")
                print(book.get_details())

                print("-----------------------------------")

        if not found:
            print("Book not found.")

    def borrow_book(self):

        while True:

            given_id = get_int()

            for book in self.books:

                if book.id == given_id:
                    book.borrow()
                    return

            print("Book not found. Please enter another ID.")


    def return_book(self):

        while True:

            given_id = get_int()

            for book in self.books:

                if book.id == given_id:

                    if isinstance(book, Returnable):
                        book.return_book()
                    else:
                        print("This book cannot be returned.")

                    return

            print("Book ID not found. Please enter another ID.")

