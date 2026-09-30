import sqlite3
import psycopg2


SQLITE_DB = "library.db"

POSTGRES_DB = "library_db"
POSTGRES_USER = "rahat"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"


sqlite_conn = sqlite3.connect(SQLITE_DB)
sqlite_conn.row_factory = sqlite3.Row

pg_conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)

pg_cursor = pg_conn.cursor()


# --------------------
# Migrate books
# --------------------

books = sqlite_conn.execute(
    "SELECT * FROM books"
).fetchall()

for book in books:
    pg_cursor.execute("""
        INSERT INTO books (
            id,
            title,
            author,
            type,
            shelf_number,
            file_size,
            copy_number,
            available
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        book["id"],
        book["title"],
        book["author"],
        book["type"],
        book["shelf_number"],
        book["file_size"],
        book["copy_number"],
        book["available"]
    ))


# --------------------
# Migrate members
# --------------------

members = sqlite_conn.execute(
    "SELECT * FROM members"
).fetchall()

for member in members:
    pg_cursor.execute("""
        INSERT INTO members (
            id,
            name,
            email,
            password_hash,
            role
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        member["id"],
        member["name"],
        member["email"],
        member["password_hash"],
        member["role"]
    ))


# --------------------
# Migrate borrow records
# --------------------

records = sqlite_conn.execute(
    "SELECT * FROM borrow_records"
).fetchall()

for record in records:
    pg_cursor.execute("""
        INSERT INTO borrow_records (
            id,
            book_id,
            member_id,
            borrowed_at,
            returned_at
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        record["id"],
        record["book_id"],
        record["member_id"],
        record["borrowed_at"],
        record["returned_at"]
    ))


pg_conn.commit()

sqlite_conn.close()
pg_cursor.close()
pg_conn.close()

print("Migration completed successfully!")
print(f"Books migrated: {len(books)}")
print(f"Members migrated: {len(members)}")
print(f"Borrow records migrated: {len(records)}")