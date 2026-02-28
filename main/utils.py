from re import findall

def tokenize (text : str) -> list [str] :
    text = text.lower ()
    words = findall (r"\b[a-z]+\b", text)
    return words