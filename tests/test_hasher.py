"""Tests for the real bcrypt password hasher."""

import pytest

from auth.hasher import BcryptPasswordHasher


@pytest.fixture(name="hasher")
def fixture_hasher() -> BcryptPasswordHasher:
    """Return a real hasher with a low cost so tests run fast."""
    return BcryptPasswordHasher(rounds=4)


def test_hash_is_not_the_plain_password(hasher: BcryptPasswordHasher) -> None:
    saved = hasher.hash("secret123")
    assert saved != "secret123"
    assert saved.startswith("$2b$")


def test_same_password_gives_different_hashes(hasher: BcryptPasswordHasher) -> None:
    first = hasher.hash("secret123")
    second = hasher.hash("secret123")
    assert first != second


def test_verify_accepts_right_password(hasher: BcryptPasswordHasher) -> None:
    saved = hasher.hash("secret123")
    assert hasher.verify("secret123", saved) is True


def test_verify_rejects_wrong_password(hasher: BcryptPasswordHasher) -> None:
    saved = hasher.hash("secret123")
    assert hasher.verify("wrong", saved) is False
