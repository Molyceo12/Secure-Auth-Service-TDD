# Secure Auth Service (TDD)

A small, reusable **user authentication library** in Python: registration and login
with **bcrypt** password hashing, a password policy, custom errors and structured
logging. Built with strict **Test-Driven Development** and **SOLID** design.

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Tests](https://img.shields.io/badge/tests-20%20passed-brightgreen)

---

## Features

- `register(username, password)`: password policy (min. 8 characters), duplicate check,
  bcrypt hashing; only the hash is stored
- `login(username, password)`: verifies the password against the stored hash
- Custom errors: `UserAlreadyExistsError`, `InvalidPasswordError`, `UserNotFoundError`
  (all inherit from `AuthError`)
- Structured logging of registrations and login attempts (passwords are never logged)
- Storage and hashing are injected, so they can be swapped or mocked

## Setup

```bash
git clone https://github.com/Molyceo12/Secure-Auth-Service-TDD.git
cd Secure-Auth-Service-TDD
python -m pip install poetry          # if Poetry is not installed
python -m poetry install
python -m poetry run python -m pre_commit install
```

Without Poetry: `python -m pip install -r requirements.txt` then `python -m pip install -e .`

## Usage

```python
from auth.hasher import BcryptPasswordHasher
from auth.repository import InMemoryUserRepository
from auth.service import UserService

service = UserService(InMemoryUserRepository(), BcryptPasswordHasher())

service.register("alice", "secret123")   # User(username='alice', password_hash='$2b$12$...')
service.login("alice", "secret123")      # returns the same user
service.login("alice", "wrong-pass")     # InvalidPasswordError
service.register("bob", "123")           # InvalidPasswordError (too short)
service.register("alice", "secret123")   # UserAlreadyExistsError
service.login("carol", "secret123")      # UserNotFoundError
```

### Demo

Run every case with one command:

```bash
python -m poetry run python examples/demo.py
```

```
      log: INFO user registered username=alice
[OK]  register alice / secret123       -> alice (hash $2b$12$qetZY...)
[ERR] register alice again             -> UserAlreadyExistsError: Username already taken: alice
[ERR] register bob / 123 (too short)   -> InvalidPasswordError: Password must be at least 8 characters
      log: INFO login succeeded username=alice
[OK]  login alice / secret123          -> alice (hash $2b$12$qetZY...)
      log: WARNING login failed username=alice reason=wrong password
[ERR] login alice / wrong-pass         -> InvalidPasswordError: Wrong password
      log: WARNING login failed username=carol reason=unknown user
[ERR] login carol (not registered)     -> UserNotFoundError: No user named carol
```

## SOLID architecture

```
                 ┌───────────────┐
   your code ──► │  UserService  │  register / login, password policy, logging
                 └───┬───────┬───┘
       depends on    │       │    depends on
      (interfaces)   ▼       ▼
        ┌────────────────┐ ┌────────────────┐
        │ UserRepository │ │ PasswordHasher │   ABCs in interfaces.py
        └───────┬────────┘ └───────┬────────┘
                ▼                  ▼
   InMemoryUserRepository   BcryptPasswordHasher   concrete implementations
```

| Principle | How it is applied |
|---|---|
| **S**ingle responsibility | the service holds the rules; the repository stores; the hasher hashes |
| **O**pen/closed | a new storage (e.g. a database) is a new `UserRepository`; the service does not change |
| **L**iskov substitution | any repository / hasher (real or mock) works in `UserService` |
| **I**nterface segregation | two small interfaces: `get`/`add` and `hash`/`verify` |
| **D**ependency inversion | `UserService(repository, hasher)` receives abstractions through its constructor (dependency injection) |

| File | Content |
|---|---|
| `src/auth/models.py` | `User` dataclass (`username`, `password_hash`) |
| `src/auth/exceptions.py` | `AuthError` and the 3 custom errors |
| `src/auth/interfaces.py` | `UserRepository`, `PasswordHasher` |
| `src/auth/repository.py` | `InMemoryUserRepository` |
| `src/auth/hasher.py` | `BcryptPasswordHasher` |
| `src/auth/service.py` | `UserService` |

## Security notes

- Passwords are hashed with **bcrypt** (cost 12) and a **new random salt** each time,
  so equal passwords give different hashes
- Verification uses `bcrypt.checkpw` (constant-time comparison)
- Plain passwords are **never stored or logged**; logs only contain usernames and events

## TDD process

Every feature followed **red → green → refactor**, and the commit history shows it
(`test: ... (red)` → `feat: ... (green)` → `refactor: ...`):

| Feature | 🔴 Red | 🟢 Green |
|---|---|---|
| Register | register hashes the password and saves the user | register users with hashed passwords |
| Duplicates | registering an existing username raises UserAlreadyExistsError | reject duplicate usernames |
| Password policy | short passwords raise InvalidPasswordError | enforce a minimum password length |
| Storage | in-memory repository stores and finds users | add InMemoryUserRepository |
| Hashing | bcrypt hasher hashes and verifies passwords | add BcryptPasswordHasher |
| Login | login returns the user for the right password | log in users with the right password |
| Unknown user | login with unknown username raises UserNotFoundError | reject unknown usernames on login |
| Wrong password | login with wrong password raises InvalidPasswordError | reject wrong passwords on login |
| Logging | auth events are logged without passwords | log registrations and login attempts |

Red commits contain the failing test and only an empty stub, so pre-commit (mypy)
still passes while the test fails for the right reason.

| 🔴 Red | 🟢 Green |
|---|---|
| ![Register red](assets/tdd/01-register-red.png) | ![Register green](assets/tdd/02-register-green.png) |
| ![Duplicate red](assets/tdd/03-duplicate-red.png) | ![Duplicate green](assets/tdd/04-duplicate-green.png) |
| ![Policy red](assets/tdd/05-password-policy-red.png) | ![Policy green](assets/tdd/06-password-policy-green.png) |
| ![Login red](assets/tdd/07-login-red.png) | ![Login green](assets/tdd/08-login-green.png) |
| ![Logging red](assets/tdd/09-logging-red.png) | ![Final coverage](assets/tdd/10-final-coverage.png) |

## Testing

```bash
python -m poetry run python -m pytest -v
python -m poetry run python -m pytest --cov --cov-report=term-missing
```

**20 tests, 100% statement and branch coverage** (the run fails below 100%), see
[`reports/coverage.txt`](reports/coverage.txt).

| Test file | Covers | Techniques |
|---|---|---|
| `test_registration.py` | register, duplicates, password policy | `pytest-mock` (mocked repository and hasher), `parametrize`, `pytest.raises` |
| `test_login.py` | login success and failures | `pytest-mock`, `pytest.raises` |
| `test_logging.py` | each auth event is logged, no passwords in logs | `caplog`, autouse fixture |
| `test_repository.py` | in-memory storage | plain asserts |
| `test_hasher.py` | real bcrypt hashing and verification | fixture |
| `test_integration.py` | register + login with real parts | no mocks |

Shared fixtures in `tests/conftest.py` provide a mocked repository, a mocked hasher
and a service wired to them.

## Code quality

Black, ruff, pylint and mypy (strict) run on every commit through pre-commit:

```bash
python -m poetry run python -m pre_commit run --all-files
```

All public classes and methods have Google-style docstrings and type hints.

## Git workflow

Git Flow: `main` (releases), `develop` (integration), short `feature/*` branches merged
into `develop` through pull requests with a simulated code review (line comments → fix
commit → sign-off).

| PR | Branch | Content |
|---|---|---|
| #1 | `chore/project-setup` | tooling, bcrypt, pre-commit, PR template |
| #2 | `feature/registration` | interfaces, register, repository, bcrypt hasher |
| #3 | `feature/login` | login, errors, logging |
| #4 | `docs/coverage-and-readme` | demo, docstrings, README, coverage report |

Releases go from `develop` to `main` through `release/*` and are tagged (`v1.0.0`).
