# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

-

## [v0.6.4] - 2026-04-26

### Changed

- Updated `CHANGELOG.md`.

## [v0.6.3] - 2026-04-22

### Changed

- Updated `requirements.txt` dependency pinning.

## [v0.6.2] - 2026-03-16

### Changed

- Updated GUI results layout to use relative positioning.
- Results panel is now read-only during display.
- Added settings panel with folder selection and persistence via `remember.json`.

## [v0.6.1] - 2026-03-15

### Added

- Added on-screen results display in the GUI.

### Changed

- Updated `README.md`, Sphinx config, and related docs to match the GUI results
 flow.

## [v0.6.0] - 2026-03-15

### Added

- Added GUI home screen entrypoint in `main/app.py`.
- Added UI scaffold and on-screen results panel.

## [v0.5.2] - 2026-03-09

### Added

- Added CLI flag `--ext` to filter output by extension (repeatable).
- Added CLI flag `--top-k` to limit displayed ranked results.
- Added CLI flag `--json` to dump each query result set to `main/results.json`.

### Changed

- Updated `--help` panel text to reflect file-dump behavior for `--json`.
- Updated project docs (`README.md` and Sphinx config) for `0.5.2`.

## [v0.5.1] - 2026-03-09

### Added

- Added CLI flag `--help` to render an in-app help panel.
- Added CLI flag `--no-colour` to disable colored output.
- Added CLI flag `--version` to print the current app version and exit.
- Added quit confirmation prompt:
  - `y` exits the app
  - `n` runs a literal search for `quit`

### Changed

- Updated help panel usage and flags section to document current CLI options.

## [v0.5.0] - 2026-03-02

### Added

- Added module and function docstrings across `main/*.py` following the
established project docstring style.
- Added Sphinx source pages for INDEXOR modules in `sphinx/source/`.

### Changed

- Updated no-results CLI message in `main/main.py` to `404. That's an error.`
- Updated `README.md` output section to match current CLI behavior.
- Updated Sphinx documentation structure and autodoc module mapping for the
package layout.

## [v0.4.1] - 2026-03-02

### Added

- Added `LICENSE` (MIT).

## [v0.4.0] - 2026-03-02

### Added

- Added `+` adjacency requirement semantics in query parsing:
  - `left + right` marks both adjacent clauses as required.

### Changed

- Updated ranked search filtering to enforce required terms and required phrases
from `+` clauses.
- Updated README query documentation and examples for `+` behavior.

## [v0.3.1] - 2026-03-01

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

## [v0.3.0] - 2026-03-01

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

## [v0.2.2] - 2026-02-28

### Added

- Added quoted-query parsing in `main/utils.py` via `parse_query`.
- Added phrase-search logic in `main/search.py` using positional matching.

### Changed

- Updated CLI output in `main/main.py` to label results as `Word` or `Phrase` dynamically.
- Updated search flow to handle mixed queries containing both normal terms and
quoted phrases.

## [v0.2.1] - 2026-02-28

### Changed

- Expanded the .gitignore to remove other junk files.

### Deleted

- Removed `__pycache__`

## [v0.2.0] - 2026-02-28

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

## [v0.1.0] - 2026-02-28

### Added

- Initial documentation files: `README.md`, `CHANGELOG.md`, and `CONTRIBUTING.md`
- Rich console theme module at `main/console.py`
- Initial startup flow in `main/main.py` for loading/saving preferred data folder

### Changed

- Enforced immediate invalid-path rejection in prompt loop
- Persist preferences only after valid directory input

### Security

- Ignore local preference file `main/remember.json` via `.gitignore`

[v0.6.3]: https://github.com/python-neo/indexor/compare/v0.6.2...HEAD
[v0.6.2]: https://github.com/python-neo/indexor/compare/v0.6.1...v0.6.2
[v0.6.1]: https://github.com/python-neo/indexor/compare/v0.6.0...v0.6.1
[v0.6.0]: https://github.com/python-neo/indexor/compare/v0.5.2...v0.6.0
[v0.5.2]: https://github.com/python-neo/indexor/compare/v0.5.1...v0.5.2
[v0.5.1]: https://github.com/python-neo/indexor/compare/v0.5.0...v0.5.1
[v0.5.0]: https://github.com/python-neo/indexor/compare/v0.4.1...v0.5.0
[v0.4.1]: https://github.com/python-neo/indexor/compare/v0.4.0...v0.4.1
[v0.4.0]: https://github.com/python-neo/indexor/compare/v0.3.1...v0.4.0
[v0.3.1]: https://github.com/python-neo/indexor/compare/v0.3.0...v0.3.1
[v0.3.0]: https://github.com/python-neo/indexor/compare/v0.2.2...v0.3.0
[v0.2.2]: https://github.com/python-neo/indexor/compare/v0.2.1...v0.2.2
[v0.2.1]: https://github.com/python-neo/indexor/compare/v0.2.0...v0.2.1
[v0.2.0]: https://github.com/python-neo/indexor/compare/v0.1.0...v0.2.0
[v0.1.0]: https://github.com/python-neo/indexor/compare/dba0f1aadc69082541edd8cc0363878427585934...v0.1.0
