from typing import Literal, Optional
from .services.borrow_service import (
    borrow_book as borrow_book_from_db,
    return_book as return_book_from_db,
    get_borrow_history,
)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .models.book import EBook, PrintedBook, Returnable
from .models.user import User

from .services.library_service import Library

from .services.book_service import (
    get_all_books,
    get_book as get_book_from_db,
    add_book,
    delete_book as delete_book_from_db,
)

from .services.member_service import (
    get_all_members,
    get_member,
    add_member,
    delete_member as delete_member_from_db,
)


app = FastAPI(
    title="Library Management System",
    description="API for managing books and users",
    version="1.0.0"
)


# Temporary old OOP library.
# Borrow/return will be migrated later.

library = Library()
library.load_books()


class BookCreate(BaseModel):
    id: int
    title: str
    author: str
    type: Literal["printed", "ebook"]
    shelf_number: Optional[str] = None
    file_size: Optional[str] = None


class UserCreate(BaseModel):
    user_id: int
    name: str
    email: str


class BorrowRequest(BaseModel):
    member_id: int


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {
        "message": "Library Management API is running"
    }


# =========================
# BOOKS
# =========================

@app.get("/books")
def get_books():

    return get_all_books()


@app.get("/books/{book_id}")
def get_book(book_id: int):

    book = get_book_from_db(book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


@app.post("/books")
def create_book(book_data: BookCreate):

    existing_book = get_book_from_db(book_data.id)

    if existing_book is not None:
        raise HTTPException(
            status_code=400,
            detail="Book ID already exists"
        )

    copy_number = 1

    if book_data.type == "printed":

        if not book_data.shelf_number:
            raise HTTPException(
                status_code=400,
                detail="shelf_number is required for printed books"
            )

        books = get_all_books()

        for book in books:

            if (
                book["type"] == "printed"
                and book["title"].lower() == book_data.title.lower()
                and book["author"].lower() == book_data.author.lower()
            ):
                copy_number += 1

    else:

        if not book_data.file_size:
            raise HTTPException(
                status_code=400,
                detail="file_size is required for ebooks"
            )

    new_book = add_book(
        book_id=book_data.id,
        title=book_data.title,
        author=book_data.author,
        book_type=book_data.type,
        shelf_number=book_data.shelf_number,
        file_size=book_data.file_size,
        copy_number=copy_number
    )

    return {
        "message": "Book created successfully",
        "book": new_book
    }


@app.delete("/books/{book_id}")
def delete_book(book_id: int):

    deleted = delete_book_from_db(book_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {
        "message": "Book deleted successfully",
        "book_id": book_id
    }


# =========================
# USERS / MEMBERS
# =========================

@app.get("/users")
def get_users():

    return get_all_members()


@app.get("/users/{user_id}")
def get_user(user_id: int):

    member = get_member(user_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return member


@app.post("/users")
def create_user(user_data: UserCreate):

    existing_member = get_member(user_data.user_id)

    if existing_member is not None:
        raise HTTPException(
            status_code=400,
            detail="User ID already exists"
        )

    try:

        member = add_member(
            member_id=user_data.user_id,
            name=user_data.name,
            email=user_data.email
        )

    except Exception as error:

        if "UNIQUE constraint failed" in str(error):

            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        raise

    return {
        "message": "User created successfully",
        "user": member
    }


@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    deleted = delete_member_from_db(user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully",
        "user_id": user_id
    }


# =========================
# BORROW
# =========================

@app.post("/books/{book_id}/borrow")
def borrow_book(book_id: int, borrow_data: BorrowRequest):

    result = borrow_book_from_db(
        book_id=book_id,
        member_id=borrow_data.member_id
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result


# =========================
# RETURN
# =========================

@app.post("/books/{book_id}/return")
def return_book(book_id: int):

    result = return_book_from_db(book_id)

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result

@app.get("/borrow-records")
def borrow_history():

    return get_borrow_history()