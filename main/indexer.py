from pathlib import Path
from .utils import tokenize

def build_index (folder_path : str) -> dict :
    index : dict [str, dict [str, list [int]]] = {}
    for file in Path (folder_path).rglob ("*") :
        if file.suffix.lower () not in (".txt", ".md") : 
            continue

        try :
            text = file.read_text (encoding = "utf-8")
        except OSError :
            continue

        for pos, word in enumerate (tokenize (text)) :
            if word not in index :
                index [word] = {}
            if str (file) not in index [word] :
                index [word] [str (file)] = []
            index [word] [str (file)].append (pos)

    return index
