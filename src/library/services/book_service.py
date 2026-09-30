from ..database import get_connection


def get_all_books():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM books
        ORDER BY id
    """)

    books = cursor.fetchall()

    cursor.close()
    connection.close()

    return books


def get_book(book_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM books
        WHERE id = %s
    """, (book_id,))

    book = cursor.fetchone()

    cursor.close()
    connection.close()

    return book


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
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO books (
            id,
            title,
            author,
            type,
            shelf_number,
            file_size,
            copy_number
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
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

    cursor.close()
    connection.close()

    return get_book(book_id)


def delete_book(book_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM books
        WHERE id = %s
    """, (book_id,))

    connection.commit()

    deleted = cursor.rowcount > 0

    cursor.close()
    connection.close()

    return deleted