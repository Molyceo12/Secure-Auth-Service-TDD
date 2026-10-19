"""Password hashing interface (Dependency Inversion).

``UserService`` only knows this interface, so any hashing implementation
(or a test mock) can be plugged in.
"""

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Turns passwords into hashes and checks them."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash a password.

        Args:
            password: Plain password.

        Returns:
            A secure, salted hash of the password.
        """

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        """Check a password against a stored hash.

        Args:
            password: Plain password to check.
            password_hash: Hash previously returned by ``hash``.

        Returns:
            ``True`` if the password matches the hash.
        """
