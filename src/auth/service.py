"""User service: the main entry point of the authentication module."""

from auth.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from auth.interfaces import PasswordHasher, UserRepository
from auth.models import User

MIN_PASSWORD_LENGTH = 8  # password policy: shortest allowed password


class UserService:
    """Registers users and verifies their credentials."""

    def __init__(self, repository: UserRepository, hasher: PasswordHasher) -> None:
        self.repository = repository
        self.hasher = hasher

    def register(self, username: str, password: str) -> User:
        """Register a new user and return it."""
        if len(password) < MIN_PASSWORD_LENGTH:
            raise InvalidPasswordError(
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
            )
        if self.repository.get(username) is not None:
            raise UserAlreadyExistsError(f"Username already taken: {username}")
        user = User(username, self.hasher.hash(password))
        self.repository.add(user)
        return user

    def login(self, username: str, password: str) -> User:
        """Return the user if the password is correct."""
        user = self.repository.get(username)
        if user is None:
            raise UserNotFoundError(f"No user named {username}")
        if self.hasher.verify(password, user.password_hash):
            return user
        raise NotImplementedError("wrong passwords come in the next cycle")
