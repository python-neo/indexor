from pathlib import Path
from .utils import tokenize

def build_index (folder_path : str) -> tuple [dict, dict, int, float] :
    """
    Build the inverted index and BM25 document statistics.

    Scans the folder recursively and indexes `.txt` and `.md` files.

    Parameters :
        folder_path (str) : Root folder path to scan.

    Returns :
        tuple [dict, dict, int, float] :
            - Inverted index as `{word : {file_path : [positions]}}`
            - Document lengths as `{file_path : token_count}`
            - Total indexed document count
            - Average document length
    """
    index : dict [str, dict [str, list [int]]] = {}
    doc_lens = {}

    for file in Path (folder_path).rglob ("*") :
        if file.suffix.lower () not in (".txt", ".md") : 
            continue

        try :
            text = file.read_text (encoding = "utf-8")
        except OSError :
            continue

        words = tokenize (text)
        doc_lens [str (file)] = len (words)
        
        for pos, word in enumerate (words) :
            if word not in index :
                index [word] = {}
            if str (file) not in index [word] :
                index [word] [str (file)] = []
            index [word] [str (file)].append (pos)

    N = len (doc_lens)
    avg_doc_len = (sum (doc_lens.values ()) / N) if N else 0.0
    return index, doc_lens, N, avg_doc_len
