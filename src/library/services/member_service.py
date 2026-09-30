from ..database import get_connection


def get_all_members():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM members
        ORDER BY id
    """)

    members = cursor.fetchall()

    cursor.close()
    connection.close()

    return members


def get_member(member_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM members
        WHERE id = %s
    """, (member_id,))

    member = cursor.fetchone()

    cursor.close()
    connection.close()

    return member


def add_member(
    member_id,
    name,
    email,
    password_hash=None,
    role="member"
):
    connection = get_connection()
    cursor = connection.cursor()

    if member_id is None:

        cursor.execute("""
            INSERT INTO members (
                name,
                email,
                password_hash,
                role
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (
            name,
            email,
            password_hash,
            role
        ))

        member_id = cursor.fetchone()["id"]

    else:

        cursor.execute("""
            INSERT INTO members (
                id,
                name,
                email,
                password_hash,
                role
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            member_id,
            name,
            email,
            password_hash,
            role
        ))

    connection.commit()

    cursor.close()
    connection.close()

    return get_member(member_id)


def delete_member(member_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM members
        WHERE id = %s
    """, (member_id,))

    connection.commit()

    deleted = cursor.rowcount > 0

    cursor.close()
    connection.close()

    return deleted


def get_member_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM members
        WHERE email = %s
    """, (email,))

    member = cursor.fetchone()

    cursor.close()
    connection.close()

    return member