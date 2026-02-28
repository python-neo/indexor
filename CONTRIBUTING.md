# Contributing to INDEXOR

Thanks for contributing. This project is intentionally simple, so please keep changes small, readable, and focused.

## Development Setup

1. Ensure Python 3.10+ is installed.
2. Clone the repository and open the project folder.
3. Run the app:

```bash
python main.py
```

## Code Style

- Keep modules focused (`indexer.py`, `search.py`, `utils.py`, `main.py`).
- Prefer clear names over clever shortcuts.
- Avoid adding heavy dependencies unless clearly justified.
- Keep behavior backward-compatible unless the change is intentional and documented.

## Suggested Workflow

1. Create a branch for your change.
2. Make focused commits.
3. Update docs when behavior changes.
4. Add or update tests when test infrastructure is introduced.
5. Open a pull request with:
   - What changed
   - Why it changed
   - How to validate it

## Reporting Issues

When filing an issue, include:

- Expected behavior
- Actual behavior
- Steps to reproduce
- Python version
- OS/environment details

## Pull Request Checklist

- Change is scoped and minimal.
- README/usage docs updated if needed.
- Changelog updated (if user-facing behavior changed).
- Manual verification steps included.
