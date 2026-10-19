"""Tests for login (storage and hashing are mocked)."""

from unittest.mock import MagicMock

import pytest

from auth.exceptions import InvalidPasswordError, UserNotFoundError
from auth.models import User
from auth.services import UserService

ALICE = User("alice", "stored-hash")


def test_login_returns_user_for_right_password(
    service: UserService, repository: MagicMock, hasher: MagicMock
) -> None:
    repository.get.return_value = ALICE
    hasher.verify.return_value = True

    assert service.login("alice", "secret123") == ALICE
    hasher.verify.assert_called_once_with("secret123", "stored-hash")


def test_login_unknown_username_raises(service: UserService, hasher: MagicMock) -> None:
    with pytest.raises(UserNotFoundError):
        service.login("bob", "secret123")

    hasher.verify.assert_not_called()


def test_login_wrong_password_raises(
    service: UserService, repository: MagicMock, hasher: MagicMock
) -> None:
    repository.get.return_value = ALICE
    hasher.verify.return_value = False

    with pytest.raises(InvalidPasswordError):
        service.login("alice", "wrong-pass")
