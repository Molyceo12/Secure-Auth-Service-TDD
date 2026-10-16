"""Tests for structured logging of auth events."""

import logging
from unittest.mock import MagicMock

import pytest

from auth.exceptions import InvalidPasswordError, UserNotFoundError
from auth.models import User
from auth.service import UserService


def test_auth_events_are_logged_without_passwords(
    service: UserService,
    repository: MagicMock,
    hasher: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO, logger="auth.service")
    service.register("alice", "secret123")
    repository.get.return_value = User("alice", "hashed")
    hasher.verify.side_effect = [True, False]
    service.login("alice", "secret123")
    with pytest.raises(InvalidPasswordError):
        service.login("alice", "wrong-pass")
    repository.get.return_value = None
    with pytest.raises(UserNotFoundError):
        service.login("bob", "secret123")

    assert [(r.levelname, r.getMessage()) for r in caplog.records] == [
        ("INFO", "user registered username=alice"),
        ("INFO", "login succeeded username=alice"),
        ("WARNING", "login failed username=alice reason=wrong password"),
        ("WARNING", "login failed username=bob reason=unknown user"),
    ]
    assert "secret123" not in caplog.text
    assert "wrong-pass" not in caplog.text
