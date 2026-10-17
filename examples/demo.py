"""Demo of the auth module: run every registration and login case once.

Usage:
    python -m poetry run python examples/demo.py
"""

import logging
from collections.abc import Callable

from auth.exceptions import (
    AuthError,
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from auth.hasher import BcryptPasswordHasher
from auth.models import User
from auth.repository import InMemoryUserRepository
from auth.service import UserService


class ListHandler(logging.Handler):
    """Collects log records so they can be printed in a table."""

    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


def print_table(title: str, headers: list[str], rows: list[list[str]]) -> None:
    """Print rows as a bordered text table with a title bar."""
    widths = [
        max([len(header), *(len(row[i]) for row in rows)])
        for i, header in enumerate(headers)
    ]
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def line(cells: list[str]) -> str:
        padded = (f" {c:<{w}} " for c, w in zip(cells, widths, strict=True))
        return "|" + "|".join(padded) + "|"

    print(f"\n:: {title} ".ljust(len(border), ":"))
    print(border)
    print(line(headers))
    print(border.replace("-", "="))
    for row in rows:
        print(line(row))
    print(border)


handler = ListHandler()
auth_logger = logging.getLogger("auth")
auth_logger.setLevel(logging.INFO)
auth_logger.addHandler(handler)

service = UserService(InMemoryUserRepository(), BcryptPasswordHasher())

# (case, action, expected outcome: None = success, else the error it must raise)
Case = tuple[str, Callable[[], User], type[AuthError] | None]

registration_cases: list[Case] = [
    ("alice / secret123", lambda: service.register("alice", "secret123"), None),
    (
        "bob / exactly8 (8 chars, minimum)",
        lambda: service.register("bob", "exactly8"),
        None,
    ),
    (
        "alice again (name taken)",
        lambda: service.register("alice", "other-pass"),
        UserAlreadyExistsError,
    ),
    (
        "carol / 1234567 (7 chars)",
        lambda: service.register("carol", "1234567"),
        InvalidPasswordError,
    ),
    (
        "dave / empty password",
        lambda: service.register("dave", ""),
        InvalidPasswordError,
    ),
]

login_cases: list[Case] = [
    ("alice / secret123", lambda: service.login("alice", "secret123"), None),
    ("bob / exactly8", lambda: service.login("bob", "exactly8"), None),
    (
        "alice / wrong-pass",
        lambda: service.login("alice", "wrong-pass"),
        InvalidPasswordError,
    ),
    (
        "alice / SECRET123 (wrong case)",
        lambda: service.login("alice", "SECRET123"),
        InvalidPasswordError,
    ),
    (
        "carol (was rejected at register)",
        lambda: service.login("carol", "1234567"),
        UserNotFoundError,
    ),
    (
        "Alice (usernames are case-sensitive)",
        lambda: service.login("Alice", "secret123"),
        UserNotFoundError,
    ),
]

logs: list[list[str]] = []
counts = {"cases": 0, "ok": 0, "rejected": 0, "pass": 0}


def run(cases: list[Case]) -> list[list[str]]:
    """Run each case, compare with the expected outcome, and collect its logs."""
    rows: list[list[str]] = []
    for title, action, expected in cases:
        counts["cases"] += 1
        number = str(counts["cases"])
        handler.records.clear()
        try:
            user = action()
            outcome: type[AuthError] | None = None
            actual = f"OK ({user.password_hash[:10]}...)"
            counts["ok"] += 1
        except AuthError as error:
            outcome = type(error)
            actual = f"{outcome.__name__}: {error}"
            counts["rejected"] += 1
        check = "PASS" if outcome is expected else "FAIL"
        counts["pass"] += check == "PASS"
        wanted = "OK" if expected is None else expected.__name__
        rows.append([number, title, wanted, actual, check])
        for record in handler.records:
            logs.append([number, record.levelname, record.getMessage()])
    return rows


CASE_HEADERS = ["#", "Case", "Expected", "Actual", "Check"]
print_table("REGISTRATION", CASE_HEADERS, run(registration_cases))
print_table("LOGIN", CASE_HEADERS, run(login_cases))
print_table("AUTH LOGS (no passwords are ever logged)", ["#", "Level", "Message"], logs)
print(
    f"\nSummary: {counts['cases']} cases | {counts['ok']} succeeded | "
    f"{counts['rejected']} rejected | {counts['pass']}/{counts['cases']} "
    "behaved as expected\n"
)
