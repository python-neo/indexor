from .utils import parse_query

def search (query : str, index : dict [str, dict]) -> dict [str, list [str]] :
    results : dict = {}
    terms, phrases = parse_query (query)

    for word in terms :
        if word in index :
            results [word] = list (index [word].keys ())
        else :
            results [word] = []

    for phrase in phrases :
        words = phrase.split ()

        if not words :
            results [f"\"{phrase}\""] = []
            continue

        if any (w not in index for w in words) :
            results [f'"{phrase}"'] = []
            continue

        files = set (index [words [0]].keys ())
        for w in words [1:] :
            files &= set (index [w].keys ())

        matched : list [str] = []

        for file in files :
            starts = index [words [0]] [file]
            ok_file = False

            for p in starts :
                ok_phrase = True
                for i, w in enumerate (words [1:], start = 1) :
                    if (p + i) not in index [w] [file] :
                        ok_phrase = False
                        break
                if ok_phrase :
                    ok_file = True
                    break

            if ok_file :
                matched.append (file)

        results [f"\"{phrase}\""] = matched

    return results