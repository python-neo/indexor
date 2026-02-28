from .utils import tokenize

def search (query : str, index : dict [str, dict [str, list]]) -> dict :
    results : dict [str, list [str]] = {}

    for word in tokenize (query) :
        if word in index :
            results [word] = list (index [word].keys ())
        else :
            results [word] = []

    return results