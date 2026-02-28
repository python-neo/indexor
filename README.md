# INDEXOR

`INDEXOR` is a lightweight Python text search project that builds an inverted index from `.txt` files and lets you search by word from the command line.

## Project Structure

```text
indexor/
|
|-- main.py
|-- indexer.py
|-- search.py
|-- utils.py
`-- data/
```

Put your `.txt` files inside the `data/` folder.

## How It Works

1. `indexer.py` scans all `.txt` files under `data/`.
2. `utils.py` tokenizes text into lowercase alphabetical words.
3. `search.py` matches query words against the index.
4. `main.py` provides an interactive CLI loop.

## Requirements

- Python 3.8+

## Run

From inside the project folder:

```bash
python main.py
```

Example query:

```text
black hole war
```

The tool returns matching files for each query word separately.

## Current Limitations

- No ranking/scoring of results.
- No phrase/proximity matching.
- Index is rebuilt on each run.
- Supports `.txt` files only.

## Roadmap Ideas

- Persist index to disk.
- Add TF-IDF or BM25 ranking.
- Support phrase search.
- Add tests and CLI flags.
