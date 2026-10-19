"""Concurrent registrations must not let two users take the same username."""

import threading
import time
from concurrent.futures import ThreadPoolExecutor

from auth.exceptions import UserAlreadyExistsError
from auth.hashing import BcryptPasswordHasher
from auth.models import User
from auth.repositories import InMemoryUserRepository
from auth.services import UserService

THREADS = 10


class SlowRepository(InMemoryUserRepository):
    """Pauses in ``get`` so threads overlap and a race shows up every time."""

    def get(self, username: str) -> User | None:
        """Wait briefly, then look up the user like the real repository."""
        time.sleep(0.01)
        return super().get(username)


def test_concurrent_registrations_of_one_username_allow_only_one() -> None:
    """Ten threads register one username: one succeeds, the rest are duplicates."""
    service = UserService(SlowRepository(), BcryptPasswordHasher(rounds=4))
    start = threading.Barrier(THREADS)

    def register() -> str:
        """Register alice once all threads are ready; report the outcome."""
        start.wait()
        try:
            service.register("alice", "secret123")
        except UserAlreadyExistsError:
            return "duplicate"
        return "ok"

    with ThreadPoolExecutor(max_workers=THREADS) as pool:
        results = [
            future.result()
            for future in [pool.submit(register) for _ in range(THREADS)]
        ]

    assert results.count("ok") == 1
    assert results.count("duplicate") == THREADS - 1
