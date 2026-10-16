"""Password hashing with bcrypt."""

from auth.interfaces import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    """Hashes and checks passwords with bcrypt."""

    def __init__(self, rounds: int = 12) -> None:
        self.rounds = rounds

    def hash(self, password: str) -> str:
        """Return a salted bcrypt hash of the password."""
        raise NotImplementedError(self.rounds)

    def verify(self, password: str, password_hash: str) -> bool:
        """Return ``True`` if the password matches the hash."""
        raise NotImplementedError(self.rounds)
