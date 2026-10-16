"""User service: the main entry point of the authentication module."""

from auth.exceptions import UserAlreadyExistsError
from auth.interfaces import PasswordHasher, UserRepository
from auth.models import User


class UserService:
    """Registers users and verifies their credentials."""

    def __init__(self, repository: UserRepository, hasher: PasswordHasher) -> None:
        self.repository = repository
        self.hasher = hasher

    def register(self, username: str, password: str) -> User:
        """Register a new user and return it."""
        if self.repository.get(username) is not None:
            raise UserAlreadyExistsError(f"Username already taken: {username}")
        user = User(username, self.hasher.hash(password))
        self.repository.add(user)
        return user
