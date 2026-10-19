"""Data models for the authentication service."""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """A registered user.

    Attributes:
        username: Unique name the user logs in with.
        password_hash: bcrypt hash of the password (never the plain password).
    """

    username: str
    password_hash: str
