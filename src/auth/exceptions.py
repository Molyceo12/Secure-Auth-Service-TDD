"""Custom exceptions raised by the authentication service."""


class AuthError(Exception):
    """Base class for all authentication errors."""


class UserAlreadyExistsError(AuthError):
    """Raised when registering a username that is already taken."""


class InvalidPasswordError(AuthError):
    """Raised when a password breaks the password policy."""


class UserNotFoundError(AuthError):
    """Raised when logging in with a username that is not registered."""
