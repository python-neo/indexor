from json import load, dump, JSONDecodeError
from pathlib import Path
from rich.prompt import Prompt
from .console import console
from .indexer import build_index
from .search import search
from rich.panel import Panel
from argparse import ArgumentParser

def main (debug) -> None :
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
        index, doc_lens, N, avg_doc_len = build_index (str (folder))
    if debug :
        console.print ("Index built.", style = "success")

    while True :
        query = Prompt.ask ("[prompt]Search (or type 'exit')[/]", console = console).strip ()
        if query.lower () == "exit" : 
            return

        results = search (query, index, doc_lens, N, avg_doc_len)
        if not results :
            console.print ("[warning]Oops! No results hiding here.[/]")
            continue

        for file, score in results :
            if debug :
                console.print (f"[path]{file}[/] - [info]{score:.4f}[/]")
            else :
                console.print (f"[path]{file}[/]")

if __name__ == "__main__" :
    argparse = ArgumentParser ()
    argparse.add_argument ("--debug", action = "store_true", help = "Debug flag for developers.")
    args = argparse.parse_args ()
    debug = args.debug
    console.print (Panel ("Welcome to INDEXOR!", title = "[title]Indexor[/]", padding = (0, 1)))
    main (debug)