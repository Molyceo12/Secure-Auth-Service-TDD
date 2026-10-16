"""In-memory user storage."""

from auth.interfaces import UserRepository
from auth.models import User


class InMemoryUserRepository(UserRepository):
    """Keeps users in a dictionary (lost when the program stops)."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def get(self, username: str) -> User | None:
        """Return the user with this username, or ``None`` if there is none."""
        return self._users.get(username)

    def add(self, user: User) -> None:
        """Store a new user."""
        self._users[user.username] = user
