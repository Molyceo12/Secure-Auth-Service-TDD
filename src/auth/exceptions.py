"""Custom exceptions raised by the authentication service."""


class AuthError(Exception):
    """Base class for all authentication errors."""


class UserAlreadyExistsError(AuthError):
    """Raised when registering a username that is already taken."""
