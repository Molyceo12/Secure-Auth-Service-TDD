"""Tests for user registration."""

import pytest
from pytest_mock import MockerFixture

from auth.exceptions import InvalidPasswordError, UserAlreadyExistsError
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


def test_register_existing_username_raises(mocker: MockerFixture) -> None:
    repository = mocker.create_autospec(UserRepository, instance=True)
    hasher = mocker.create_autospec(PasswordHasher, instance=True)
    repository.get.return_value = User("alice", "old-hash")

    with pytest.raises(UserAlreadyExistsError):
        UserService(repository, hasher).register("alice", "secret123")

    repository.add.assert_not_called()
    hasher.hash.assert_not_called()


@pytest.mark.parametrize("password", ["", "short", "1234567"])
def test_register_short_password_raises(mocker: MockerFixture, password: str) -> None:
    repository = mocker.create_autospec(UserRepository, instance=True)
    hasher = mocker.create_autospec(PasswordHasher, instance=True)
    repository.get.return_value = None

    with pytest.raises(InvalidPasswordError):
        UserService(repository, hasher).register("alice", password)

    hasher.hash.assert_not_called()


def test_register_accepts_password_of_minimum_length(mocker: MockerFixture) -> None:
    repository = mocker.create_autospec(UserRepository, instance=True)
    hasher = mocker.create_autospec(PasswordHasher, instance=True)
    repository.get.return_value = None
    hasher.hash.return_value = "hashed"

    assert UserService(repository, hasher).register("alice", "12345678").username == (
        "alice"
    )
