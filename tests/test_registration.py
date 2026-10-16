"""Tests for user registration."""

from pytest_mock import MockerFixture

from auth.interfaces import PasswordHasher, UserRepository
from auth.models import User
from auth.service import UserService


def test_register_hashes_password_and_saves_user(mocker: MockerFixture) -> None:
    repository = mocker.create_autospec(UserRepository, instance=True)
    hasher = mocker.create_autospec(PasswordHasher, instance=True)
    repository.get.return_value = None
    hasher.hash.return_value = "hashed"

    user = UserService(repository, hasher).register("alice", "secret123")

    assert user == User("alice", "hashed")
    hasher.hash.assert_called_once_with("secret123")
    repository.add.assert_called_once_with(user)
