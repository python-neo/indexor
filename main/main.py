from json import load, dump, JSONDecodeError
from pathlib import Path
from rich.prompt import Prompt
from .console import console
from .indexer import build_index
from .search import search
from rich.panel import Panel
from argparse import ArgumentParser

def get_result_title (file_path : Path) -> str :
    """
    Resolve display title for a result file.

    For Markdown files, the first `# Heading` line is preferred.
    Otherwise, title is derived from filename stem.

    Parameters :
        file_path (Path) : Resolved file path.

    Returns :
        str : Display title.
    """
    if file_path.suffix.lower () in (".md", ".markdown") :
        try :
            with file_path.open ("r", encoding = "utf-8") as f :
                first_line = f.readline ().strip ()
            if first_line.startswith ("#") :
                heading = first_line.lstrip ("#").strip ()
                if heading :
                    return heading
        except (OSError, UnicodeError) :
            pass

    stem = file_path.stem.replace ("_", " ").strip ()
    return stem.title () if stem else file_path.stem

def main (debug) -> None :
    """
    Run the INDEXOR interactive CLI loop.

    Loads persisted folder preferences, builds index statistics, accepts
    search queries, and renders ranked results.

    Parameters :
        debug (bool) : Enables debug output such as scoring details.
    """
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
            console.print ("[warning]404. That's an error.[/]")
            continue

        for i, (file, score) in enumerate (results) :
            file_path = Path (file).resolve ()
            try :
                shown = str (file_path.relative_to (folder))
            except ValueError :
                shown = str (file_path)

            title = get_result_title (file_path)
            if i > 0 :
                console.print ("")
            console.print (f"[title]{title}[/]")

            if debug :
                console.print (f"[path]{shown}[/] - [info]{score:.4f}[/]")
            else :
                console.print (f"[path]{shown}[/]")

if __name__ == "__main__" :
    argparse = ArgumentParser ()
    argparse.add_argument ("--debug", action = "store_true", help = "Debug flag for developers.")
    args = argparse.parse_args ()
    debug = args.debug
    console.print (Panel ("[success]Welcome to INDEXOR![/]", title = "[title]Indexor[/]", padding = (0, 1)))
    main (debug)
