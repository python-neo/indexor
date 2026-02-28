from json import load, dump, JSONDecodeError
from pathlib import Path
from rich.prompt import Prompt
from .console import console

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
            raw = Prompt.ask ("Enter folder path for future searches", console = console).strip ()

        if not raw :
            console.print ("Invalid folder path. Please enter an existing directory.", style = "error")
            data ["path"] = ""
            continue

        folder = Path (raw).expanduser ()
        folder = (Path.cwd () / folder).resolve () if not folder.is_absolute () else folder.resolve ()

        if not folder.exists () or not folder.is_dir () :
            console.print ("Invalid folder path. Please enter an existing directory.", style = "error")
            data ["path"] = ""
            continue

        data ["path"] = str (folder)
        with remember.open ("w", encoding = "utf-8") as f :
            dump (data, f, indent = 4)
        return

if __name__ == "__main__" :
    main ()
