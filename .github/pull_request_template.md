## What

<!-- What does this PR change? -->

## Why

<!-- Why is the change needed? -->

## TDD cycle

- [ ] Red: a failing test was committed first
- [ ] Green: the minimum code to make it pass
- [ ] Refactor: code cleaned up, all tests still pass

## How to test

```bash
python -m poetry run python -m pytest --cov
```

## Review checklist

- [ ] All tests pass and coverage is 100% (statements and branches)
- [ ] Type hints and Google-style docstrings on new code
- [ ] No plain-text passwords stored or logged
- [ ] Pre-commit passes (Black, ruff, pylint, mypy)
