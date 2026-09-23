from ..database import get_connection


def borrow_book(book_id, member_id):
    connection = get_connection()

    try:
        # 1. Check whether the book exists
        book = connection.execute("""
            SELECT *
            FROM books
            WHERE id = ?
        """, (book_id,)).fetchone()

        if book is None:
            return {
                "success": False,
                "message": "Book not found"
            }

        # 2. Check whether the member exists
        member = connection.execute("""
            SELECT *
            FROM members
            WHERE id = ?
        """, (member_id,)).fetchone()

        if member is None:
            return {
                "success": False,
                "message": "Member not found"
            }

        # 3. Check whether the book is available
        if book["available"] == 0:
            return {
                "success": False,
                "message": "Book is already borrowed"
            }

        # 4. Create borrow record
        connection.execute("""
            INSERT INTO borrow_records (
                book_id,
                member_id
            )
            VALUES (?, ?)
        """, (
            book_id,
            member_id
        ))

        # 5. Mark book as unavailable
        connection.execute("""
            UPDATE books
            SET available = 0
            WHERE id = ?
        """, (book_id,))

        # 6. Save both changes
        connection.commit()

        return {
            "success": True,
            "message": "Book borrowed successfully"
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def return_book(book_id, member_id):
    connection = get_connection()

    try:
        # 1. Check whether the book exists
        book = connection.execute("""
            SELECT *
            FROM books
            WHERE id = ?
        """, (book_id,)).fetchone()

        if book is None:
            return {
                "success": False,
                "message": "Book not found"
            }

        # 2. Find the active borrow record
        borrow_record = connection.execute("""
    SELECT *
    FROM borrow_records
    WHERE book_id = ?
    AND member_id = ?
    AND returned_at IS NULL
    ORDER BY id DESC
    LIMIT 1
""", (book_id, member_id)).fetchone()

        if borrow_record is None:
            return {
                "success": False,
                "message": "Book is not currently borrowed"
            }

        # 3. Mark the borrow record as returned
        connection.execute("""
            UPDATE borrow_records
            SET returned_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (borrow_record["id"],))

        # 4. Make the book available again
        connection.execute("""
            UPDATE books
            SET available = 1
            WHERE id = ?
        """, (book_id,))

        # 5. Save both changes
        connection.commit()

        return {
            "success": True,
            "message": "Book returned successfully"
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_borrow_history():
    connection = get_connection()

    records = connection.execute("""
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
    """).fetchall()

    connection.close()

    return [dict(record) for record in records]