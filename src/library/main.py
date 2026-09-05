
from .models.book import EBook, PrintedBook, Returnable
from .services.library_service import Library

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

