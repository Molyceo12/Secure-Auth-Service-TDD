"""User service: the main entry point of the authentication module."""

import logging

from auth.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from auth.interfaces import PasswordHasher, UserRepository
from auth.models import User

MIN_PASSWORD_LENGTH = 8  # password policy: shortest allowed password
logger = logging.getLogger(__name__)


class UserService:
    """Registers users and verifies their credentials."""

    def __init__(self, repository: UserRepository, hasher: PasswordHasher) -> None:
        self.repository = repository
        self.hasher = hasher

    def register(self, username: str, password: str) -> User:
        """Register a new user with a hashed password.

        Args:
            username: Name the user will log in with; must not be taken.
            password: Plain password; at least ``MIN_PASSWORD_LENGTH`` characters.

        Returns:
            The saved user (only the password hash is stored).

        Raises:
            InvalidPasswordError: If the password is too short.
            UserAlreadyExistsError: If the username is already registered.
        """
        if len(password) < MIN_PASSWORD_LENGTH:
            raise InvalidPasswordError(
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
            )
        if self.repository.get(username) is not None:
            raise UserAlreadyExistsError(f"Username already taken: {username}")
        user = User(username, self.hasher.hash(password))
        self.repository.add(user)
        logger.info("user registered username=%s", username)
        return user

    def login(self, username: str, password: str) -> User:
        """Check a user's credentials.

        Args:
            username: Registered username.
            password: Plain password to check against the stored hash.

        Returns:
            The user, if the password is correct.

        Raises:
            UserNotFoundError: If no user has this username.
            InvalidPasswordError: If the password is wrong.
        """
        user = self.repository.get(username)
        if user is None:
            logger.warning("login failed username=%s reason=unknown user", username)
            raise UserNotFoundError(f"No user named {username}")
        if not self.hasher.verify(password, user.password_hash):
            logger.warning("login failed username=%s reason=wrong password", username)
            raise InvalidPasswordError("Wrong password")
        logger.info("login succeeded username=%s", username)
        return user
