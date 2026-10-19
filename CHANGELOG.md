# Changelog

## [2.0.0] - 2026-10-19

Code split into packages; test docstrings.

### Changed
- Modules grouped into `hashing/`, `models/`, `repositories/`, `services/` and
  `utils/` packages, each interface in its own `base.py`; import paths changed
- Tests split into `tests/unit/` and `tests/integration/`

### Added
- A one-line docstring on every test function

## [1.0.0] - 2026-10-18

First release of the secure authentication module, built with strict TDD.

### Added
- `UserService.register`: password policy (minimum 8 characters), duplicate-username
  check and bcrypt hashing; only the hash is stored
- `UserService.login`: verifies the password against the stored hash
- Custom errors: `AuthError`, `UserAlreadyExistsError`, `InvalidPasswordError`,
  `UserNotFoundError`
- `UserRepository` and `PasswordHasher` interfaces with `InMemoryUserRepository` and
  `BcryptPasswordHasher` implementations (dependency injection, SOLID)
- Structured logging: INFO for successful registration and login, WARNING for failed
  registration and login; passwords are never logged
- Thread-safe registration: a lock makes the username check and save one step
- Demo (`examples/demo.py`): 11 registration and login cases shown in tables with
  expected and actual outcomes, logs and a summary

### Quality
- 23 tests, 100% statement and branch coverage (the run fails below 100%)
- Unit tests with `pytest-mock`, plus integration and concurrency tests
- Pre-commit: black, ruff, pylint, mypy (strict)
