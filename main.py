books = []

def add_book():
    while True:
        id_exists = False
        given_id = int(input("Please enter an Id: "))
        for book in books:
            if book["id"] == given_id:
                id_exists = True
                print(f"This ID already exists. Please enter a new ID.")
                break
        if not id_exists:
            break
                
    title = input("Give a Book Title: ")
    author = input("Give an Author Name: ")
    
    create_book = {
        "id" : given_id,
        "title" : title,
        "author" : author,
        "available" : True
    }
    
    books.append(create_book)
    print("The book is successfully added")
    print(create_book)

def view_available_books():
    total_books = 0 
    for book in books:
        if book["available"]: 
            total_books += 1 
            print(book)
    if total_books == 0:
        print("No book available")
    else:
        print("Total Book:",total_books)
        
def search_book():
        search_term = input("Search a book: ").lower()
        found = False
        for book in books:
            if(
                str(book["id"]) == search_term
                or search_term in book["title"].lower()
                or search_term in book["author"].lower()
                ):
                    found = True
                    print(book)
        
        if not found:
                print("not found")
def borrow_book():
    while True:
        given_id = int(input("Please enter an Id: "))

        for book in books:
            if book["id"] == given_id:

                if book["available"]:
                    book["available"] = False
                    print("Book borrowed successfully")
                else:
                    print("Book is already borrowed")

                return

        print("Book not found. Please enter another ID.")

    
def return_book():
    while True:
        give_id = int(input("Give book id: "))
        id_found = False
        for book in books:
            if book["id"] == give_id:
                id_found = True
                if book["available"]:
                    print("this is already availabe. can not return")
                else:
                    book["available"] = True
                    print("Book returned successfully")
                break
        if not id_found:
            print("Book Id not found")
        else:
            break


def main():
    while True:
        print('''================================
      LIBRARY MANAGEMENT
================================

1. Add Book
2. View Available Books
3. Search Book
4. Borrow Book
5. Return Book
6. Exit''')

        choice_option = int(input("Enter your choice: "))

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
            break
        else:
            print("Invalid Option. Please Try again")

main()

        
        