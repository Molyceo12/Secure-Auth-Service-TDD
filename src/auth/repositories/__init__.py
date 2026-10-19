"""User storage: the repository interface and its implementations."""

from auth.repositories.base import UserRepository
from auth.repositories.in_memory_repository import InMemoryUserRepository

__all__ = ["InMemoryUserRepository", "UserRepository"]
