"""Password hashing with bcrypt."""

import bcrypt

from auth.interfaces import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    """Hashes and checks passwords with bcrypt."""

    def __init__(self, rounds: int = 12) -> None:
        self.rounds = rounds

    def hash(self, password: str) -> str:
        """Return a salted bcrypt hash of the password."""
        salt = bcrypt.gensalt(rounds=self.rounds)
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify(self, password: str, password_hash: str) -> bool:
        """Return ``True`` if the password matches the hash."""
        return bcrypt.checkpw(password.encode(), password_hash.encode())
