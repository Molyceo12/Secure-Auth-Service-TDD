"""In-memory user storage."""

from auth.models import User
from auth.repositories.base import UserRepository


class InMemoryUserRepository(UserRepository):
    """Keeps users in a dictionary (data is lost when the program stops)."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def get(self, username: str) -> User | None:
        """Find a user by username.

        Args:
            username: Name to look up.

        Returns:
            The user, or ``None`` if there is no user with that name.
        """
        return self._users.get(username)

    def add(self, user: User) -> None:
        """Store a new user.

        Args:
            user: The user to store.
        """
        self._users[user.username] = user
