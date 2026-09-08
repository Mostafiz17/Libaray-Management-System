from src.library.models.user import User


def test_user_creation():
    user = User(1, "Mostafiz", "mostafiz@example.com")

    assert user.user_id == 1
    assert user.name == "Mostafiz"
    assert user.email == "mostafiz@example.com"


def test_user_string():
    user = User(1, "Mostafiz", "mostafiz@example.com")

    assert str(user) == "ID: 1, Name: Mostafiz, Email: mostafiz@example.com"
