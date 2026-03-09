# INDEXOR

`INDEXOR` is a lightweight CLI search tool that builds an inverted index over `.txt` and `.md` files and returns ranked matches using BM25.

## Requirements

- Python 3.10+

Install dependencies:

```bash
pip install -r requirements.txt
```

## Project Structure

```text
Indexor/
|
|-- main/
|   |-- __init__.py
|   |-- main.py
|   |-- indexer.py
|   |-- search.py
|   |-- utils.py
|   |-- console.py
|   `-- remember.json (generated locally)
|-- README.md
|-- CHANGELOG.md
`-- CONTRIBUTING.md
```

## How It Works

1. `main/main.py` loads/saves your preferred folder path in `main/remember.json`.
2. `main/indexer.py` recursively scans the folder for `.txt` and `.md` files.
3. `main/utils.py` tokenizes text to lowercase alphabetic words.
4. `main/search.py` parses normal terms and quoted phrases, enforces required clauses, and ranks files with BM25.
5. Results are printed as a ranked list of file paths.

## Run

From the project root:

```bash
python -m main.main
```

Optional flags:

```bash
python -m main.main --debug
python -m main.main --help
python -m main.main --no-colour
python -m main.main --version
python -m main.main --ext md --top-k 10
python -m main.main --json
```

On first run, you will be prompted for a folder path to index. That path is stored in `main/remember.json` and reused in future runs.

Flag summary:

- `--debug`: print BM25 score beside each result
- `--help`: show the in-app help panel and exit
- `--no-colour`: disable all colored terminal output
- `--version`: print current INDEXOR version and exit
- `--ext`: filter output by extension (repeatable, e.g. `--ext md --ext txt`)
- `--top-k`: show only top `N` ranked results
- `--json`: dump each query's results to `main/results.json` while keeping normal terminal output

## Query Example

Input:

```text
"black hole" + space spaceship
```

Output behavior:

- Returns a ranked file list for the whole query
- Quoted phrases are checked using positional adjacency
- `+` marks both adjacent clauses as required (`left + right`)
  - Example: `"black hole" + space spaceship`
  - required: `"black hole"` and `space`
  - optional: `spaceship` (still affects ranking if present)
- Each result shows a title above the path:
  - Markdown files use first-line `# Heading` when available
  - Other files use formatted filename (no extension, underscores removed, title-cased)
- Paths are shown relative to the indexed folder
- Blank line is inserted between results for readability
- In `--debug`, scores are printed beside each file
- Shows `404. That's an error.` if nothing matches
- Typing `quit` asks:
  - `y` to quit
  - `n` to search for the literal term `quit`
- When `--json` is set, each query also writes structured output to `main/results.json`

## Current Limitations

- No proximity/slop phrase matching (only exact quoted phrases)
- Index is rebuilt every run
- UTF-8 text reading only

## Roadmap Ideas

- Persist and reuse built index
- Add configurable ranking options
- Add advanced phrase operators (proximity/slop)
- Add automated tests
