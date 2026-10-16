"""Shared fixtures: a service wired to mocked storage and hashing."""

from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from auth.interfaces import PasswordHasher, UserRepository
from auth.service import UserService


@pytest.fixture(name="repository")
def fixture_repository(mocker: MockerFixture) -> MagicMock:
    """Return a mocked repository that starts with no users."""
    repository: MagicMock = mocker.create_autospec(UserRepository, instance=True)
    repository.get.return_value = None
    return repository


@pytest.fixture(name="hasher")
def fixture_hasher(mocker: MockerFixture) -> MagicMock:
    """Return a mocked hasher whose hashes are ``"hashed"``."""
    hasher: MagicMock = mocker.create_autospec(PasswordHasher, instance=True)
    hasher.hash.return_value = "hashed"
    return hasher


@pytest.fixture(name="service")
def fixture_service(repository: MagicMock, hasher: MagicMock) -> UserService:
    """Return a service using the mocked repository and hasher."""
    return UserService(repository, hasher)
