"""Tests for user registration (storage and hashing are mocked)."""

from unittest.mock import MagicMock

import pytest

from auth.exceptions import InvalidPasswordError, UserAlreadyExistsError
from auth.models import User
from auth.service import UserService


def test_register_hashes_password_and_saves_user(
    service: UserService, repository: MagicMock, hasher: MagicMock
) -> None:
    user = service.register("alice", "secret123")

    assert user == User("alice", "hashed")
    hasher.hash.assert_called_once_with("secret123")
    repository.add.assert_called_once_with(user)


def test_register_existing_username_raises(
    service: UserService, repository: MagicMock, hasher: MagicMock
) -> None:
    repository.get.return_value = User("alice", "old-hash")

    with pytest.raises(UserAlreadyExistsError):
        service.register("alice", "secret123")

    repository.add.assert_not_called()
    hasher.hash.assert_not_called()


@pytest.mark.parametrize("password", ["", "short", "1234567"])
def test_register_short_password_raises(
    service: UserService, hasher: MagicMock, password: str
) -> None:
    with pytest.raises(InvalidPasswordError):
        service.register("alice", password)

    hasher.hash.assert_not_called()


def test_register_accepts_password_of_minimum_length(service: UserService) -> None:
    assert service.register("alice", "12345678").username == "alice"
