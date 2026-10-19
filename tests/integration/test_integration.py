"""End-to-end: register and log in with the real repository and bcrypt."""

import pytest

from auth.exceptions import InvalidPasswordError, UserAlreadyExistsError
from auth.hashing import BcryptPasswordHasher
from auth.repositories import InMemoryUserRepository
from auth.services import UserService


def test_register_then_login_with_real_parts() -> None:
    """Register, log in, reject a wrong password and a duplicate, with real parts."""
    service = UserService(InMemoryUserRepository(), BcryptPasswordHasher(rounds=4))

    user = service.register("alice", "secret123")

    assert user.password_hash.startswith("$2b$")
    assert service.login("alice", "secret123") == user
    with pytest.raises(InvalidPasswordError):
        service.login("alice", "wrong-pass")
    with pytest.raises(UserAlreadyExistsError):
        service.register("alice", "another-pass")
