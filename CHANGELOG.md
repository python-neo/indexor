# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

-

## [0.2.0] - 2026-02-28

### Added (0.2.0)

- `requirements.txt` with pinned `rich` dependency.
- Search implementation in `main/search.py` for token-to-file lookups.

### Changed (0.2.0)

- Updated startup/runtime flow in `main/main.py`:
  - reads/writes `main/remember.json`
  - validates directory input and loops prompt on invalid paths
  - builds index with a Rich spinner
  - adds welcome panel before entering the CLI loop
- Updated `main/indexer.py` to recursively index `.txt` and `.md` files.
- Updated project docs:
  - `README.md` now reflects package layout and `python -m main.main` usage
  - `CONTRIBUTING.md` now uses `pip install -r requirements.txt` and module run command
- Renamed GitLab pipeline file from `.gitlab_ci.yml` to `.gitlab-ci.yml`.
- `.gitignore` now excludes `main/__pycache__/` in addition to `main/remember.json`.

## [0.1.0] - 2026-02-28

### Added (0.1.0)

- Initial documentation files: `README.md`, `CHANGELOG.md`, and `CONTRIBUTING.md`
- Rich console theme module at `main/console.py`
- Initial startup flow in `main/main.py` for loading/saving preferred data folder

### Changed (0.1.0)

- Enforced immediate invalid-path rejection in prompt loop
- Persist preferences only after valid directory input

### Security (0.1.0)

- Ignore local preference file `main/remember.json` via `.gitignore`
