from ..database import get_connection


def get_all_books():
    connection = get_connection()

    books = connection.execute("""
        SELECT *
        FROM books
        ORDER BY id
    """).fetchall()

    connection.close()

    return [dict(book) for book in books]


def get_book(book_id):
    connection = get_connection()

    book = connection.execute("""
        SELECT *
        FROM books
        WHERE id = ?
    """, (book_id,)).fetchone()

    connection.close()

    if book is None:
        return None

    return dict(book)


def add_book(
    book_id,
    title,
    author,
    book_type,
    shelf_number=None,
    file_size=None,
    copy_number=1
):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO books (
            id,
            title,
            author,
            type,
            shelf_number,
            file_size,
            copy_number
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        book_id,
        title,
        author,
        book_type,
        shelf_number,
        file_size,
        copy_number
    ))

    connection.commit()

    connection.close()

    return get_book(book_id)


def delete_book(book_id):
    connection = get_connection()

    cursor = connection.execute("""
        DELETE FROM books
        WHERE id = ?
    """, (book_id,))

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted