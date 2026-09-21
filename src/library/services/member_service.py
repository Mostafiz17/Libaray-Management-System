from ..database import get_connection


def get_all_members():
    connection = get_connection()

    members = connection.execute("""
        SELECT *
        FROM members
        ORDER BY id
    """).fetchall()

    connection.close()

    return [dict(member) for member in members]


def get_member(member_id):
    connection = get_connection()

    member = connection.execute("""
        SELECT *
        FROM members
        WHERE id = ?
    """, (member_id,)).fetchone()

    connection.close()

    if member is None:
        return None

    return dict(member)


def add_member(member_id, name, email):
    connection = get_connection()

    connection.execute("""
        INSERT INTO members (
            id,
            name,
            email
        )
        VALUES (?, ?, ?)
    """, (
        member_id,
        name,
        email
    ))

    connection.commit()
    connection.close()

    return get_member(member_id)


def delete_member(member_id):
    connection = get_connection()

    cursor = connection.execute("""
        DELETE FROM members
        WHERE id = ?
    """, (member_id,))

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted