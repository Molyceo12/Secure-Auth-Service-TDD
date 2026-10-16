"""Abstractions the service depends on (Dependency Inversion)."""

from abc import ABC, abstractmethod

from auth.models import User


class UserRepository(ABC):
    """Storage for users."""

    @abstractmethod
    def get(self, username: str) -> User | None:
        """Return the user with this username, or ``None`` if there is none."""

    @abstractmethod
    def add(self, user: User) -> None:
        """Store a new user."""


class PasswordHasher(ABC):
    """Turns passwords into hashes and checks them."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Return a secure hash of the password."""

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        """Return ``True`` if the password matches the hash."""
