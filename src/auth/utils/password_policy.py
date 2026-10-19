"""Password policy rules shared by the service."""

MIN_PASSWORD_LENGTH = 8  # shortest allowed password


def is_password_long_enough(password: str) -> bool:
    """Check a password against the minimum length rule.

    Args:
        password: Plain password to check.

    Returns:
        ``True`` if the password has at least ``MIN_PASSWORD_LENGTH`` characters.
    """
    return len(password) >= MIN_PASSWORD_LENGTH
