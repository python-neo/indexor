# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

-

## [0.1.0] - 2026-02-28

### Added

- Initial documentation files: `README.md`, `CHANGELOG.md`, and `CONTRIBUTING.md`
- Rich console theme module at `main/console.py`
- Initial startup flow in `main/main.py` for loading/saving preferred data folder

### Changed

- Enforced immediate invalid-path rejection in prompt loop
- Persist preferences only after valid directory input

### Security

- Ignore local preference file `main/remember.json` via `.gitignore`
