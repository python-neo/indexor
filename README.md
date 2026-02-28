# INDEXOR

`INDEXOR` is a lightweight CLI search tool that builds an inverted index over `.txt` and `.md` files.

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
4. `main/search.py` searches query tokens in the built index.
5. Results are printed per query word in the CLI.

## Run

From the project root:

```bash
python -m main.main
```

On first run, you will be prompted for a folder path to index. That path is stored in `main/remember.json` and reused in future runs.

## Query Example

Input:

```text
black hole war
```

Output behavior:

- Prints each query word
- Shows matching file paths for each word
- Shows `No files found.` if none match

## Current Limitations

- No ranking/scoring of results
- No phrase/proximity matching
- Index is rebuilt every run
- UTF-8 text reading only

## Roadmap Ideas

- Persist and reuse built index
- Add ranked retrieval (TF-IDF/BM25)
- Add phrase search
- Add automated tests
