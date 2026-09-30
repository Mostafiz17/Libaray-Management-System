from ..database import get_connection


def borrow_book(book_id, member_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT *
            FROM books
            WHERE id = %s
        """, (book_id,))

        book = cursor.fetchone()

        if book is None:
            return {
                "success": False,
                "message": "Book not found"
            }

        cursor.execute("""
            SELECT *
            FROM members
            WHERE id = %s
        """, (member_id,))

        member = cursor.fetchone()

        if member is None:
            return {
                "success": False,
                "message": "Member not found"
            }

        if book["available"] == 0:
            return {
                "success": False,
                "message": "Book is already borrowed"
            }

        cursor.execute("""
            INSERT INTO borrow_records (
                book_id,
                member_id
            )
            VALUES (%s, %s)
        """, (
            book_id,
            member_id
        ))

        cursor.execute("""
            UPDATE books
            SET available = 0
            WHERE id = %s
        """, (book_id,))

        connection.commit()

        return {
            "success": True,
            "message": "Book borrowed successfully"
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def return_book(book_id, member_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT *
            FROM books
            WHERE id = %s
        """, (book_id,))

        book = cursor.fetchone()

        if book is None:
            return {
                "success": False,
                "message": "Book not found"
            }

        cursor.execute("""
            SELECT *
            FROM borrow_records
            WHERE book_id = %s
            AND member_id = %s
            AND returned_at IS NULL
            ORDER BY id DESC
            LIMIT 1
        """, (book_id, member_id))

        borrow_record = cursor.fetchone()

        if borrow_record is None:
            return {
                "success": False,
                "message": "Book is not currently borrowed"
            }

        cursor.execute("""
            UPDATE borrow_records
            SET returned_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (borrow_record["id"],))

        cursor.execute("""
            UPDATE books
            SET available = 1
            WHERE id = %s
        """, (book_id,))

        connection.commit()

        return {
            "success": True,
            "message": "Book returned successfully"
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def get_borrow_history():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            borrow_records.id,
            books.title AS book_title,
            members.name AS member_name,
            borrow_records.borrowed_at,
            borrow_records.returned_at
        FROM borrow_records
        JOIN books
            ON borrow_records.book_id = books.id
        JOIN members
            ON borrow_records.member_id = members.id
        ORDER BY borrow_records.id DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return records