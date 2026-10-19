"""User storage interface (Dependency Inversion).

``UserService`` only knows this interface, so any storage implementation
(or a test mock) can be plugged in.
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
