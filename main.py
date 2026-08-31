books = []


def get_int():
    while True:
        try:
            value = int(input("Please enter an ID: "))
        except ValueError:
            print("This is not an integer.")
            continue

        if value <= 0:
            print("ID must be a positive integer.")
            continue

        return value


def add_book():
    while True:
        given_id = get_int()

        id_exists = False

        for book in books:
            if book["id"] == given_id:
                id_exists = True
                break

        if id_exists:
            print("This ID already exists. Please enter a new ID.")
            continue

        break

    title = input("Give a Book Title: ").strip()
    author = input("Give an Author Name: ").strip()

    create_book = {
        "id": given_id,
        "title": title,
        "author": author,
        "available": True
    }

    books.append(create_book)

    print("\nThe book was successfully added.")
    print(create_book)


def view_available_books():
    total_books = 0

    print("\n========== AVAILABLE BOOKS ==========")

    for book in books:
        if book["available"]:
            total_books += 1

            print(f"ID: {book['id']}")
            print(f"Title: {book['title']}")
            print(f"Author: {book['author']}")
            print("Status: Available")
            print("-----------------------------------")

    if total_books == 0:
        print("No books are currently available.")
    else:
        print(f"Total available books: {total_books}")


def search_book():
    search_term = input("Search for a book: ").strip().lower()

    found = False

    for book in books:

        if (
            search_term in str(book["id"]).lower()
            or search_term in book["title"].lower()
            or search_term in book["author"].lower()
        ):
            found = True

            print("\nBook Found")
            print(f"ID: {book['id']}")
            print(f"Title: {book['title']}")
            print(f"Author: {book['author']}")

            if book["available"]:
                print("Status: Available")
            else:
                print("Status: Borrowed")

            print("-----------------------------------")

    if not found:
        print("Book not found.")


def borrow_book():
    while True:
        given_id = get_int()

        for book in books:

            if book["id"] == given_id:

                if book["available"]:
                    book["available"] = False
                    print("Book borrowed successfully.")
                else:
                    print("Book is already borrowed.")

                return

        print("Book not found. Please enter another ID.")


def return_book():
    while True:
        given_id = get_int()

        for book in books:

            if book["id"] == given_id:

                if book["available"]:
                    print("This book is already available.")
                else:
                    book["available"] = True
                    print("Book returned successfully.")

                return

        print("Book ID not found. Please enter another ID.")


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
            choice_option = int(input("Enter your choice: "))

        except ValueError:
            print("Please enter a number.")
            continue

        if not 1 <= choice_option <= 6:
            print("Invalid option. Please try again.")
            continue

        if choice_option == 1:
            add_book()

        elif choice_option == 2:
            view_available_books()

        elif choice_option == 3:
            search_book()

        elif choice_option == 4:
            borrow_book()

        elif choice_option == 5:
            return_book()

        elif choice_option == 6:
            print("Thank you for using the Library Management System.")
            break


if __name__ == "__main__":
    main()