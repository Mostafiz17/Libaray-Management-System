from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .models.book import EBook, PrintedBook, Returnable
from .models.user import User
from .services.library_service import Library
from .services.user_service import UserService


app = FastAPI(
    title="Library Management System",
    description="API for managing books and users",
    version="1.0.0"
)


library = Library()
library.load_books()

user_service = UserService()
user_service.load_users()


class BookCreate(BaseModel):
    id: int
    title: str
    author: str
    type: Literal["printed", "ebook"]
    shelf_number: str | None = None
    file_size: str | None = None


class UserCreate(BaseModel):
    user_id: int
    name: str
    email: str


@app.get("/")
def home():
    return {
        "message": "Library Management API is running"
    }


@app.get("/books")
def get_books():
    return [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "details": book.get_details(),
            "available": book.is_available()
        }
        for book in library.books
    ]


@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in library.books:
        if book.id == book_id:
            return {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "details": book.get_details(),
                "available": book.is_available()
            }

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


@app.post("/books")
def create_book(book_data: BookCreate):
    for book in library.books:
        if book.id == book_data.id:
            raise HTTPException(
                status_code=400,
                detail="Book ID already exists"
            )

    if book_data.type == "printed":
        if not book_data.shelf_number:
            raise HTTPException(
                status_code=400,
                detail="shelf_number is required for printed books"
            )

        copy_number = 1

        for book in library.books:
            if (
                isinstance(book, PrintedBook)
                and book.title.lower() == book_data.title.lower()
                and book.author.lower() == book_data.author.lower()
            ):
                copy_number += 1

        new_book = PrintedBook(
            book_data.id,
            book_data.title,
            book_data.author,
            book_data.shelf_number,
            copy_number
        )

    else:
        if not book_data.file_size:
            raise HTTPException(
                status_code=400,
                detail="file_size is required for ebooks"
            )

        new_book = EBook(
            book_data.id,
            book_data.title,
            book_data.author,
            book_data.file_size
        )

    library.books.append(new_book)
    library.save_books()

    return {
        "message": "Book created successfully",
        "book": {
            "id": new_book.id,
            "title": new_book.title,
            "author": new_book.author,
            "details": new_book.get_details(),
            "available": new_book.is_available()
        }
    }


@app.post("/books/{book_id}/borrow")
def borrow_book(book_id: int):
    for book in library.books:
        if book.id == book_id:
            if not book.is_available():
                raise HTTPException(
                    status_code=400,
                    detail="Book is already borrowed"
                )

            book.borrow()
            library.save_books()

            return {
                "message": "Book borrowed successfully",
                "book_id": book_id
            }

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


@app.post("/books/{book_id}/return")
def return_book(book_id: int):
    for book in library.books:
        if book.id == book_id:
            if not isinstance(book, Returnable):
                raise HTTPException(
                    status_code=400,
                    detail="This book cannot be returned"
                )

            if book.is_available():
                raise HTTPException(
                    status_code=400,
                    detail="Book is already available"
                )

            book.return_book()
            library.save_books()

            return {
                "message": "Book returned successfully",
                "book_id": book_id
            }

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


@app.get("/users")
def get_users():
    return [
        {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email
        }
        for user in user_service.users
    ]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = user_service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email
    }


@app.post("/users")
def create_user(user_data: UserCreate):
    if user_service.get_user(user_data.user_id):
        raise HTTPException(
            status_code=400,
            detail="User ID already exists"
        )

    user = User(
        user_data.user_id,
        user_data.name,
        user_data.email
    )

    user_service.add_user(user)
    user_service.save_users()

    return {
        "message": "User created successfully",
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email
        }
    }