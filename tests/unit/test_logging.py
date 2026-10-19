"""Tests that auth events are logged (and passwords never are)."""

import logging
from unittest.mock import MagicMock

import pytest

from auth.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from auth.models import User
from auth.services import UserService


@pytest.fixture(autouse=True)
def capture_info_logs(caplog: pytest.LogCaptureFixture) -> None:
    """Record INFO and higher log lines from the service in every test."""
    caplog.set_level(logging.INFO, logger="auth.services.user_service")


def test_registration_is_logged(
    service: UserService, caplog: pytest.LogCaptureFixture
) -> None:
    """A successful registration is logged without the password."""
    service.register("alice", "secret123")
    assert "user registered username=alice" in caplog.text
    assert "secret123" not in caplog.text


def test_short_password_registration_is_logged_as_warning(
    service: UserService, caplog: pytest.LogCaptureFixture
) -> None:
    """A too-short password is logged as a warning without the password."""
    with pytest.raises(InvalidPasswordError):
        service.register("bob", "short1")
    assert caplog.records[-1].levelname == "WARNING"
    assert "registration failed username=bob reason=password too short" in caplog.text
    assert "short1" not in caplog.text


def test_duplicate_registration_is_logged_as_warning(
    service: UserService, repository: MagicMock, caplog: pytest.LogCaptureFixture
) -> None:
    """A taken username is logged as a warning without the password."""
    repository.get.return_value = User("alice", "hashed")
    with pytest.raises(UserAlreadyExistsError):
        service.register("alice", "secret123")
    assert caplog.records[-1].levelname == "WARNING"
    assert "registration failed username=alice reason=username taken" in caplog.text
    assert "secret123" not in caplog.text


def test_successful_login_is_logged(
    service: UserService,
    repository: MagicMock,
    hasher: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A successful login is logged."""
    repository.get.return_value = User("alice", "hashed")
    hasher.verify.return_value = True
    service.login("alice", "secret123")
    assert "login succeeded username=alice" in caplog.text


def test_wrong_password_is_logged_as_warning(
    service: UserService,
    repository: MagicMock,
    hasher: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A wrong password is logged as a warning without the password."""
    repository.get.return_value = User("alice", "hashed")
    hasher.verify.return_value = False
    with pytest.raises(InvalidPasswordError):
        service.login("alice", "wrong-pass")
    assert caplog.records[-1].levelname == "WARNING"
    assert "login failed username=alice reason=wrong password" in caplog.text
    assert "wrong-pass" not in caplog.text


def test_unknown_user_is_logged_as_warning(
    service: UserService, caplog: pytest.LogCaptureFixture
) -> None:
    """A login for an unknown user is logged as a warning."""
    with pytest.raises(UserNotFoundError):
        service.login("bob", "secret123")
    assert caplog.records[-1].levelname == "WARNING"
    assert "login failed username=bob reason=unknown user" in caplog.text
