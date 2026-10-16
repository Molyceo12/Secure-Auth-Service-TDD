"""Tests for the in-memory user repository."""

from auth.models import User
from auth.repository import InMemoryUserRepository


def test_repository_finds_added_users() -> None:
    repository = InMemoryUserRepository()
    repository.add(User("alice", "hash-a"))
    assert repository.get("alice") == User("alice", "hash-a")


def test_repository_returns_none_for_unknown_user() -> None:
    assert InMemoryUserRepository().get("nobody") is None
