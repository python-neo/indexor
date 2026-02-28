from json import load, dump, JSONDecodeError
from pathlib import Path
from rich.prompt import Prompt
from .console import console
from .indexer import build_index
from .search import search
from rich.panel import Panel

def main () -> None :
    remember = Path (__file__).resolve ().parent / "remember.json"
    data : dict = {}

    try :
        if remember.exists () :
            with remember.open ("r", encoding = "utf-8") as f :
                loaded = load (f)
                if isinstance (loaded, dict) :
                    data = loaded
    except JSONDecodeError :
        data = {}

    while True :
        saved = data.get ("path")
        if isinstance (saved, str) and saved.strip () :
            raw = saved.strip () 
        else :
            raw = Prompt.ask ("[prompt]Enter folder path for future searches[/]", console = console).strip ()

        if not raw :
            console.print ("[error]Invalid folder path. Please enter an existing directory.[/]")
            data ["path"] = ""
            continue

        folder = Path (raw).expanduser ()
        folder = (Path.cwd () / folder).resolve () if not folder.is_absolute () else folder.resolve ()

        if not folder.exists () or not folder.is_dir () :
            console.print ("[error]Invalid folder path. Please enter an existing directory.[/]")
            data ["path"] = ""
            continue

        data ["path"] = str (folder)
        with remember.open ("w", encoding = "utf-8") as f :
            dump (data, f, indent = 4)
        break

    with console.status ("[info]Building index...[/]", spinner = "dots") :
        index = build_index (str (folder))
    console.print ("Index built.", style = "success")

    while True :
        query = Prompt.ask ("[prompt]Search (or type 'exit')[/]", console = console).strip ()
        if query.lower () == "exit" : 
            return

        results = search (query, index)
        if not results :
            console.print ("[warning]No query words found.[/]")
            continue

        for word, files in results.items () :
            console.print (f"Word : {word}", style = "word")
            if not files :
                console.print ("    [warning]No files found.[/]")
                continue
            for file in files :
                console.print (f"  [path]{file}[/]")

if __name__ == "__main__" :
    console.print (Panel ("Welcome to INDEXOR!", title = "[title]Indexor[/]", padding = (0, 1)))
    main ()