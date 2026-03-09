from json import load, dump, JSONDecodeError
from pathlib import Path
from rich.prompt import Prompt
from .console import get_console
from .indexer import build_index
from .search import search
from rich.panel import Panel
from argparse import ArgumentParser
from textwrap import dedent

console = get_console ()

def n_file (file : str) : return file.strip ().lower ().lstrip (".")

def positive_int (text : str) -> int :
    """
    Parse a positive integer for argparse.
    """
    value = int (text)
    if value < 1 :
        raise ValueError ("Must be >= 1")
    return value

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

def print_help () -> None :
    """
    Render the CLI help panel for INDEXOR.
    """
    body = dedent ("""
        [word]Usage[/]
        python -m main.main [--debug] [--help] [--no-colour] [--version] [--ext EXT] [--top-k N] [--json]

        [word]Flags[/]
        [success]--debug[/]      Show BM25 score beside each result
        [success]--help[/]       Show this help panel
        [success]--no-colour[/]  Disable coloured output
        [success]--version[/]    Print app version and exit
        [success]--ext[/]        Filter output by extension (repeatable)
        [success]--top-k[/]      Show only top N ranked results
        [success]--json[/]       Dump results to `main/results.json`

        [word]Query Notes[/]
        - Quoted phrases are supported: [info]"black hole"[/]
        - [info]+[/] marks adjacent clauses as required
        - Type [warning]quit[/] to exit, or choose [warning]n[/] to search [warning]quit[/]
        """).strip ()
    console.print (Panel (body, title = "[title]Indexor[/]", padding = (0, 1)))

def main (debug : bool, no_colour : bool = False, exts : set | None = None, top_k : int | None = None, output_json : bool = False) -> None :
    """
    Run the INDEXOR interactive CLI loop.

    Loads persisted folder preferences, builds index statistics, accepts
    search queries, and renders ranked results.

    Parameters :
        debug (bool) : Enables debug output such as scoring details.
        no_colour (bool) : Disable coloured output when `True`.
        exts (set | None) : Restrict displayed results to these extensions.
        top_k (int | None) : Limit output to top N ranked results.
        output_json (bool) : Dump each query result set to `main/results.json`.
    """
    global console
    console = get_console (no_colour = no_colour)
    selected_exts = exts if exts is not None else set ()

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
        query = Prompt.ask ("[prompt]Search (or type 'quit')[/]", console = console).strip ()
        if query.lower () == "quit" :
            answer = Prompt.ask ("[prompt]Do you want to quit? (y = quit, n = search 'quit')[/]", choices = ["y", "n"], default = "y", console = console)
            if answer == "y" :
                return
            query = "quit"

        results = search (query, index, doc_lens, N, avg_doc_len)
        if selected_exts :
            results = [(file, score) for file, score in results if n_file (Path (file).suffix) in selected_exts]
        if top_k is not None :
            results = results [:top_k]
        if not results :
            if output_json :
                payload = {"query" : query, "count" : 0, "results" : []}
                try :
                    with (Path (__file__).resolve ().parent / "results.json").open ("w", encoding = "utf-8") as f :
                        dump (payload, f, ensure_ascii = False, indent = 4)
                except OSError :
                    console.print ("[error]Failed to write main/results.json[/]")
            console.print ("[warning]404. That's an error.[/]")
            continue

        entries : list [dict] = []
        for file, score in results :
            file_path = Path (file).resolve ()
            try :
                shown = str (file_path.relative_to (folder))
            except ValueError :
                shown = str (file_path)
            entries.append ({"title" : get_result_title (file_path), "path" : shown, "score" : score})

        if output_json :
            payload = {"query" : query, "count" : len (entries), "results" : entries}
            try :
                with (Path (__file__).resolve ().parent / "results.json").open ("w", encoding = "utf-8") as f :
                    dump (payload, f, ensure_ascii = False, indent = 4)
            except OSError :
                console.print ("[error]Failed to write main/results.json[/]")

        for i, entry in enumerate (entries) :
            if i > 0 :
                console.print ("")
            console.print (f"[title]{entry['title']}[/]")
            if debug :
                console.print (f"[path]{entry['path']}[/] - [info]{entry['score']:.4f}[/]")
            else :
                console.print (f"[path]{entry['path']}[/]")

if __name__ == "__main__" :
    argparse = ArgumentParser (add_help = False)
    argparse.add_argument ("--debug", action = "store_true", help = "Debug flag for developers.")
    argparse.add_argument ("--help", action = "store_true", help = "Show CLI help section.")
    argparse.add_argument ("--no-colour", action = "store_true", help = "Disable coloured output.")
    argparse.add_argument ("--ext", action = "append", default = None, help = "Filter output by extension; repeatable.")
    argparse.add_argument ("--top-k", type = positive_int, default = None, help = "Show only top N ranked results.")
    argparse.add_argument ("--version", action = "version", version = "Indexor 0.5.2")
    argparse.add_argument ("--json", action = "store_true", help = "Dump results to main/results.json.")
    args = argparse.parse_args ()
    console = get_console (no_colour = args.no_colour)
    if args.help :
        print_help ()
    else :
        console.print (Panel ("[success]Welcome to INDEXOR![/]", title = "[title]Indexor[/]", padding = (0, 1)))
    main (
        args.debug,
        no_colour = args.no_colour,
        exts = {n_file (ext) for ext in args.ext if ext.strip ()} if args.ext else None,
        top_k = args.top_k,
        output_json = args.json,
    )
