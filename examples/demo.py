"""Demo of the auth module: run every registration and login case once.

Usage:
    python -m poetry run python examples/demo.py
"""

import logging
import sys
from collections.abc import Callable

from auth.exceptions import AuthError
from auth.hasher import BcryptPasswordHasher
from auth.models import User
from auth.repository import InMemoryUserRepository
from auth.service import UserService

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout, format="      log: %(levelname)s %(message)s"
)
service = UserService(InMemoryUserRepository(), BcryptPasswordHasher())

cases: list[tuple[str, Callable[[], User]]] = [
    ("register alice / secret123", lambda: service.register("alice", "secret123")),
    ("register alice again", lambda: service.register("alice", "secret123")),
    ("register bob / 123 (too short)", lambda: service.register("bob", "123")),
    ("login alice / secret123", lambda: service.login("alice", "secret123")),
    ("login alice / wrong-pass", lambda: service.login("alice", "wrong-pass")),
    ("login carol (not registered)", lambda: service.login("carol", "secret123")),
]

for title, action in cases:
    try:
        user = action()
        print(
            f"[OK]  {title:<32} -> {user.username} (hash {user.password_hash[:12]}...)"
        )
    except AuthError as error:
        print(f"[ERR] {title:<32} -> {type(error).__name__}: {error}")
