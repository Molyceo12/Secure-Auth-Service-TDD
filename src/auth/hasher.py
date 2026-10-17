"""Password hashing with bcrypt."""

import bcrypt

from auth.interfaces import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    """Hashes and checks passwords with bcrypt.

    Attributes:
        rounds: bcrypt cost factor. 12 is a safe default (slow enough to resist
            brute force, fast enough for logins); tests use 4 to stay fast.
    """

    def __init__(self, rounds: int = 12) -> None:
        self.rounds = rounds

    def hash(self, password: str) -> str:
        """Hash a password with a new random salt.

        Args:
            password: Plain password.

        Returns:
            The bcrypt hash, e.g. ``$2b$12$...``.
        """
        salt = bcrypt.gensalt(rounds=self.rounds)
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify(self, password: str, password_hash: str) -> bool:
        """Check a password against a stored bcrypt hash (constant-time).

        Args:
            password: Plain password to check.
            password_hash: Hash previously returned by ``hash``.

        Returns:
            ``True`` if the password matches the hash.
        """
        return bcrypt.checkpw(password.encode(), password_hash.encode())
