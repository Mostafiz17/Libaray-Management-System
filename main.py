class Book:
    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author
        self.__available = True

    def __str__(self):
        status = "Available" if self.__available else "Borrowed"

        return (
            f"ID: {self.id}, "
            f"Title: {self.title}, "
            f"Author: {self.author}, "
            f"Status: {status}"
        )

    def borrow(self):
        if self.__available:
            self.__available = False
            print("Book borrowed successfully.")
        else:
            print("Book is already borrowed.")

    def return_book(self):
        if self.__available:
            print("Book is already available.")
        else:
            self.__available = True
            print("Book successfully returned.")

    def is_available(self):
        return self.__available


class EBook(Book):
    def __init__(self, id, title, author, file_size):
        super().__init__(id, title, author)
        self.file_size = file_size

    def __str__(self):
        status = "Available" if self.is_available() else "Borrowed"

        return (
            f"ID: {self.id}, "
            f"Title: {self.title}, "
            f"Author: {self.author}, "
            f"File Size: {self.file_size}, "
            f"Status: {status}"
        )

    def borrow(self):
        if self.is_available():
            print(f"EBook '{self.title}' downloaded successfully.")
        else:
            print("EBook is already borrowed.")


class PrintedBook(Book):
    def __init__(self, id, title, author, shelf_number):
        super().__init__(id, title, author)
        self.shelf_number = shelf_number

    def __str__(self):
        status = "Available" if self.is_available() else "Borrowed"

        return (
            f"ID: {self.id}, "
            f"Title: {self.title}, "
            f"Author: {self.author}, "
            f"Shelf: {self.shelf_number}, "
            f"Status: {status}"
        )

    def borrow(self):
        if self.is_available():
            print(
                f"Printed book '{self.title}' "
                f"has been borrowed from the library."
            )
            super().borrow()
        else:
            print("Printed book is already borrowed.")


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

        # Create object
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

                print(f"ID: {book.id}")
                print(f"Title: {book.title}")
                print(f"Author: {book.author}")

                if isinstance(book, EBook):
                    print(f"Type: EBook")
                    print(f"File Size: {book.file_size}")

                elif isinstance(book, PrintedBook):
                    print(f"Type: Printed Book")
                    print(f"Shelf: {book.shelf_number}")

                print("Status: Available")
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

                if isinstance(book, EBook):
                    print("Type: EBook")
                    print(f"File Size: {book.file_size}")

                elif isinstance(book, PrintedBook):
                    print("Type: Printed Book")
                    print(f"Shelf: {book.shelf_number}")

                if book.is_available():
                    print("Status: Available")
                else:
                    print("Status: Borrowed")

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
                    book.return_book()
                    return

            print("Book ID not found. Please enter another ID.")


library = Library()


def main():

    while True:

        print("""
================================
      LIBRARY MANAGEMENT
================================

1. Add Book
2. View Available Books
3. Search Book
4. Borrow Book
5. Return Book
6. Exit
""")

        try:
            choice_option = int(
                input("Enter your choice: ")
            )

        except ValueError:
            print("Please enter a number.")
            continue

        if not 1 <= choice_option <= 6:
            print("Invalid option. Please try again.")
            continue

        if choice_option == 1:
            library.add_book()

        elif choice_option == 2:
            library.view_available_books()

        elif choice_option == 3:
            library.search_book()

        elif choice_option == 4:
            library.borrow_book()

        elif choice_option == 5:
            library.return_book()

        elif choice_option == 6:
            print(
                "Thank you for using the Library Management System."
            )
            break


if __name__ == "__main__":
    main()