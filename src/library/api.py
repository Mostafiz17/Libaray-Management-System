from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

from typing import Literal, Optional
from .services.borrow_service import (
    borrow_book as borrow_book_from_db,
    return_book as return_book_from_db,
    get_borrow_history,
)
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
    get_member_by_email,
    add_member,
    delete_member as delete_member_from_db,
)
app = FastAPI(
    title="Library Management System",
    description="API for managing books and users",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = get_member(int(user_id))

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


def get_current_admin(
    current_user = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user


@app.get("/users")
def get_users():
    return get_all_members()

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

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str
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
def create_book(
    book_data: BookCreate,
    current_admin = Depends(get_current_admin)
):

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
def delete_book(
    book_id: int,
    current_admin = Depends(get_current_admin)
):

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

@app.get("/users/me")
def get_current_user_info(
    current_user = Depends(get_current_user)
):
    return {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

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
def create_user(
    user_data: UserCreate,
    current_admin = Depends(get_current_admin)
):

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

@app.post("/auth/register")
def register_user(register_data: RegisterRequest):

    existing_member = get_member_by_email(
        register_data.email
    )

    if existing_member is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        register_data.password
    )

    member = add_member(
        member_id=None,
        name=register_data.name,
        email=register_data.email,
        password_hash=hashed_password
    )

    return {
        "message": "User registered successfully",
        "user": {
            "id": member["id"],
            "name": member["name"],
            "email": member["email"]
        }
    }
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_admin = Depends(get_current_admin)
):
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
def borrow_book(
    book_id: int,
    current_user = Depends(get_current_user)
):

    result = borrow_book_from_db(
        book_id=book_id,
        member_id=current_user["id"]
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
def return_book(
    book_id: int,
    current_user = Depends(get_current_user)
):

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

@app.post("/auth/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    member = get_member_by_email(
        form_data.username
    )

    if member is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if member["password_hash"] is None:
        raise HTTPException(
            status_code=401,
            detail="Account has no password"
        )

    password_correct = verify_password(
        form_data.password,
        member["password_hash"]
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token({
    "sub": str(member["id"]),
    "email": member["email"],
    "role": member["role"]
})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
