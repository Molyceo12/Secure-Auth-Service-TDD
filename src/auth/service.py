"""User service: the main entry point of the authentication module."""

import logging
import threading

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
    """Registers users and verifies their credentials.

    Registration is thread-safe within one ``UserService`` instance: its lock makes
    the "is the name free?" check and the save a single step. Share one instance
    across threads; separate instances using the same repository are not protected.
    """

    def __init__(self, repository: UserRepository, hasher: PasswordHasher) -> None:
        self.repository = repository
        self.hasher = hasher
        # Makes "is the name free? -> save" one step, so two threads can't
        # register the same username at the same time.
        self._register_lock = threading.Lock()

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
        self._ensure_username_free(username)  # fail fast, before slow hashing
        user = User(username, self.hasher.hash(password))
        with self._register_lock:
            # Re-check: another thread may have taken the name while we hashed.
            self._ensure_username_free(username)
            self.repository.add(user)
        logger.info("user registered username=%s", username)
        return user

    def _ensure_username_free(self, username: str) -> None:
        """Raise ``UserAlreadyExistsError`` if the username is already registered."""
        if self.repository.get(username) is not None:
            raise UserAlreadyExistsError(f"Username already taken: {username}")

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
