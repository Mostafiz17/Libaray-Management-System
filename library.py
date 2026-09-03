from models import Book, EBook, PrintedBook, Returnable



class Library:

    def __init__(self):
        self.books = []

    def get_int(self):
        while True:
            try:
                value = int(input("Please enter an ID: "))

                if value <= 0:
                    print("ID must be a positive integer.")
                    continue

                return value

            except ValueError:
                print("Please enter a valid integer.")

    def add_book(self):

        # Get unique ID
        while True:
            given_id = self.get_int()

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

            new_book = PrintedBook(
                given_id,
                title,
                author,
                shelf_number
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

        total_books = 0

        print("\n========== AVAILABLE BOOKS ==========")

        for book in self.books:

            if book.is_available():
                total_books += 1

                print(book)
                print("-----------------------------------")

        if total_books == 0:
            print("No books are currently available.")
        else:
            print(f"Total available books: {total_books}")

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

            given_id = self.get_int()

            for book in self.books:

                if book.id == given_id:
                    book.borrow()
                    return

            print("Book not found. Please enter another ID.")


    def return_book(self):

        while True:

            given_id = self.get_int()

            for book in self.books:

                if book.id == given_id:

                    if isinstance(book, Returnable):
                        book.return_book()
                    else:
                        print("This book cannot be returned.")

                    return

            print("Book ID not found. Please enter another ID.")

