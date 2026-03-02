# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-03-02

### Added

- Added `+` adjacency requirement semantics in query parsing:
  - `left + right` marks both adjacent clauses as required.

### Changed

- Updated ranked search filtering to enforce required terms and required phrases from `+` clauses.
- Updated README query documentation and examples for `+` behavior.

## [0.3.1] - 2026-03-01

### Changed

- Updated result rendering in `main/main.py`:
  - shows result titles in `[title]` style above links
  - displays links as paths relative to the indexed folder
  - inserts a blank line between results
- Improved title generation:
  - Markdown uses first-line `# Heading` when present
  - fallback uses filename without extension, with underscores removed and title-casing
- Updated no-results message to `Oops! No results here.`

### Documentation

- Updated `README.md` output behavior to match the current UI.

## [0.3.0] - 2026-03-01

### Added

- Added BM25 ranking flow using indexed document statistics (`doc_lens`, `N`, `avg_doc_len`).
- Added debug CLI flag (`--debug`) to print per-result scores.

### Changed

- Updated search behavior to return one ranked result list for the whole query.
- Integrated quoted-phrase handling with positional checks during ranked retrieval.
- Updated `README.md` to reflect ranked output, phrase behavior, and debug usage.

### Fixed

- Fixed non-debug output path in `main/main.py` so file results print correctly 
instead of blank lines.

## [0.2.2] - 2026-02-28

### Added

- Added quoted-query parsing in `main/utils.py` via `parse_query`.
- Added phrase-search logic in `main/search.py` using positional matching.

### Changed

- Updated CLI output in `main/main.py` to label results as `Word` or `Phrase` dynamically.
- Updated search flow to handle mixed queries containing both normal terms and 
quoted phrases.

## [0.2.1] - 2026-02-28

### Changed

- Expanded the .gitignore to remove other junk files.

### Deleted

- Removed `__pycache__`

## [0.2.0] - 2026-02-28

### Added

- `requirements.txt` with pinned `rich` dependency.
- Search implementation in `main/search.py` for token-to-file lookups.

### Changed

- Updated startup/runtime flow in `main/main.py`:
  - reads/writes `main/remember.json`
  - validates directory input and loops prompt on invalid paths
  - builds index with a Rich spinner
  - adds welcome panel before entering the CLI loop
- Updated `main/indexer.py` to recursively index `.txt` and `.md` files.
- Updated project docs:
  - `README.md` now reflects package layout and `python -m main.main` usage
  - `CONTRIBUTING.md` now uses `pip install -r requirements.txt` and module run 
  command.
- Renamed GitLab pipeline file from `.gitlab_ci.yml` to `.gitlab-ci.yml`.
- `.gitignore` now excludes `main/__pycache__/` in addition to `main/remember.json`.

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
