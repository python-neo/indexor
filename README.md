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
4. `main/search.py` parses normal terms and quoted phrases, filters by phrase matches, and ranks files with BM25.
5. Results are printed as a ranked list of file paths.

## Run

From the project root:

```bash
python -m main.main
```

Optional debug mode:

```bash
python -m main.main --debug
```

On first run, you will be prompted for a folder path to index. That path is stored in `main/remember.json` and reused in future runs.

## Query Example

Input:

```text
black "black hole" war
```

Output behavior:

- Returns a ranked file list for the whole query
- Quoted phrases are checked using positional adjacency
- In `--debug`, scores are printed beside each file
- Shows `Oops! No results hiding here.` if nothing matches

## Current Limitations

- No proximity/slop phrase matching (only exact quoted phrases)
- Index is rebuilt every run
- UTF-8 text reading only

## Roadmap Ideas

- Persist and reuse built index
- Add configurable ranking options
- Add advanced phrase operators (proximity/slop)
- Add automated tests
