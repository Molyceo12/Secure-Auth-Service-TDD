"""Tests for the bcrypt password hasher (real bcrypt, low cost for speed)."""

import pytest

from auth.hasher import BcryptPasswordHasher


@pytest.fixture(name="hasher")
def fixture_hasher() -> BcryptPasswordHasher:
    """Return a hasher with a low cost so tests run fast."""
    return BcryptPasswordHasher(rounds=4)


def test_hash_is_salted_bcrypt_not_plain_text(hasher: BcryptPasswordHasher) -> None:
    first, second = hasher.hash("secret123"), hasher.hash("secret123")
    assert first != "secret123"
    assert first.startswith("$2b$04$")
    assert first != second  # a new salt every time


@pytest.mark.parametrize(
    ("password", "expected"), [("secret123", True), ("wrong", False)]
)
def test_verify_checks_password_against_hash(
    hasher: BcryptPasswordHasher, password: str, expected: bool
) -> None:
    assert hasher.verify(password, hasher.hash("secret123")) is expected
