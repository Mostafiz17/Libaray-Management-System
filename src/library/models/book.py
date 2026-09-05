from abc import ABC, abstractmethod

class Returnable(ABC):
    @abstractmethod
    def return_book(self):
        pass
class Book(ABC):
    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author

    def __str__(self):
        return (
            f"ID: {self.id}, "
            f"Title: {self.title}, "
            f"Author: {self.author}"
        )

    @abstractmethod
    def borrow(self):
        pass

    @abstractmethod
    def is_available(self):
        pass

    @abstractmethod
    def get_details(self):
        pass

class EBook(Book):
    def __init__(self, id, title, author, file_size):
        super().__init__(id, title, author)
        self.file_size = file_size

    def __str__(self):
        return (
            f"ID: {self.id}, "
            f"Title: {self.title}, "
            f"Author: {self.author}, "
            f"File Size: {self.file_size}"
        )

    def is_available(self):
        return True

    def borrow(self):
        print(f"EBook '{self.title}' downloaded successfully.")

    def get_details(self):
        return (
            f"Type: EBook\n"
            f"File Size: {self.file_size}\n"
            f"Status: Available"
        )

class PrintedBook(Book, Returnable):

    def __init__(self, id, title, author, shelf_number, copy_number=1):
        super().__init__(id, title, author)

        self.shelf_number = shelf_number
        self.copy_number = copy_number
        self.__available = True

    def __str__(self):

        status = "Available" if self.__available else "Borrowed"

        return (
            f"ID: {self.id}, "
            f"Title: {self.title}, "
            f"Author: {self.author}, "
            f"Copy: {self.copy_number}, "
            f"Shelf: {self.shelf_number}, "
            f"Status: {status}"
        )

    def borrow(self):

        if self.__available:
            self.__available = False
            print("Printed book borrowed successfully.")
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

    def get_details(self):

        status = "Available" if self.__available else "Borrowed"

        return (
            f"Type: Printed Book\n"
            f"Copy: {self.copy_number}\n"
            f"Shelf: {self.shelf_number}\n"
            f"Status: {status}"
        )