"""Tests for login (storage and hashing are mocked)."""

from unittest.mock import MagicMock

from auth.models import User
from auth.service import UserService

ALICE = User("alice", "stored-hash")


def test_login_returns_user_for_right_password(
    service: UserService, repository: MagicMock, hasher: MagicMock
) -> None:
    repository.get.return_value = ALICE
    hasher.verify.return_value = True

    assert service.login("alice", "secret123") == ALICE
    hasher.verify.assert_called_once_with("secret123", "stored-hash")
