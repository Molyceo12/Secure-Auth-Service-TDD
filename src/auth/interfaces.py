"""Abstractions the service depends on (Dependency Inversion).

``UserService`` only knows these interfaces, so any storage or hashing
implementation (or a test mock) can be plugged in.
"""

from abc import ABC, abstractmethod

from auth.models import User


class UserRepository(ABC):
    """Storage for users."""

    @abstractmethod
    def get(self, username: str) -> User | None:
        """Find a user by username.

        Args:
            username: Name to look up.

        Returns:
            The user, or ``None`` if there is no user with that name.
        """

    @abstractmethod
    def add(self, user: User) -> None:
        """Store a new user.

        Args:
            user: The user to store.
        """


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
