import os

from datetime import datetime, timedelta, timezone

import jwt

from dotenv import load_dotenv

from pwdlib import PasswordHash


load_dotenv()


password_hash = PasswordHash.recommended()


SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not configured"
    )


ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password):
    return password_hash.hash(password)


def verify_password(
    plain_password,
    hashed_password
):
    return password_hash.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data):

    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.InvalidTokenError:

        return None