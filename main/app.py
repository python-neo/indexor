import tkinter as tk
from .indexer import build_index
from pathlib import Path
from .search import search
from json import load, dump, JSONDecodeError
from threading import Thread
from tkinter import filedialog

SEARCH_DEFAULT = Path ().home () / "Desktop"
REMEMBER_FILE = Path (__file__).resolve ().parent / "remember.json"

class App :
    def __init__ (self) -> None :
        self.bg = "#000000"
        self.fg = "#29C611"
        self.root = tk.Tk ()
        self.root.title ("Indexor")
        self.root.state ("zoomed")
        self.root.config (bg = self.bg)
        self.mode = "home"
        self.search_path = self._load_saved_path ()
        self.index, self.doc_lens, self.N, self.avg_doc_len  = None, None, None, None
        Thread (target = self._build_index, daemon = True).start ()
        self.home_screen ()
    
    def _build_index (self) -> None :
        self.index, self.doc_lens, self.N, self.avg_doc_len = build_index (str (self.search_path))

    def _load_saved_path (self) -> Path :
        try :
            if REMEMBER_FILE.exists () :
                with REMEMBER_FILE.open ("r", encoding = "utf-8") as f :
                    data = load (f)
                    if isinstance (data, dict) :
                        raw = data.get ("path")
                        if isinstance (raw, str) and raw.strip () :
                            return Path (raw).expanduser ()
        except JSONDecodeError :
            pass
        return SEARCH_DEFAULT

    def _save_path (self, folder : Path) -> None :
        try :
            with REMEMBER_FILE.open ("w", encoding = "utf-8") as f :
                dump ({"path" : str (folder)}, f, indent = 4)
        except OSError :
            pass

    def home_screen (self) :
        self.search_box = tk.Frame (self.root, width = 700, height = 40, bg = self.bg, 
                                    highlightbackground = self.fg, highlightthickness = 2, 
                                    highlightcolor = self.fg)
        self.search_box.place (relx = 0.5, rely = 0.5, relwidth = 0.6, relheight = 0.06, anchor = "center")
        self.search_box.pack_propagate (False)

        self.search = tk.Entry (self.search_box, fg = self.fg, insertbackground = self.fg, 
                                relief = "flat", bg = self.bg, font = ("Consolas", 12))
        self.search.pack (fill = "both", padx = 3, pady = 8)

        self.brand = tk.Label (self.root, bg = self.bg, fg = self.fg, text = "I n d e x o r", 
                               font = ("Segoe UI", 40, "bold"))
        self.brand.place (relx = 0.5, rely = 0.4, anchor = "center")

        self.settings = tk.Button (self.root, text = "\u2699", bg = self.bg, fg = self.fg, relief = "flat",
                                    bd = 0, font = ("Segoe UI Symbol", 18), command = self.toggle_settings)
        self.settings.place (relx = 0.97, rely = 0.03, anchor = "ne")
        self.settings.lift ()

        self.settings_panel = tk.Frame (self.root, bg = self.bg, highlightbackground = self.fg, highlightthickness = 1)
        self.settings_panel.place (relx = 1.0, rely = 0.0, relwidth = 0.3, relheight = 1.0, anchor = "ne")
        self.settings_panel.place_forget ()

        header = tk.Label (self.settings_panel, text = "Settings", bg = self.bg, fg = self.fg,
                           font = ("Consolas", 16, "bold"))
        header.pack (anchor = "w", padx = 16, pady = (16, 8))

        tk.Label (self.settings_panel, text = "Index folder", bg = self.bg, fg = self.fg,
                  font = ("Consolas", 11)).pack (anchor = "w", padx = 16)
        self.path_var = tk.StringVar (value = str (self.search_path))
        self.path_entry = tk.Entry (self.settings_panel, textvariable = self.path_var, bg = self.bg, fg = self.fg,
                                    insertbackground = self.fg, relief = "flat", font = ("Consolas", 11))
        self.path_entry.pack (fill = "x", padx = 16, pady = (6, 12))

        actions = tk.Frame (self.settings_panel, bg = self.bg)
        actions.pack (fill = "x", padx = 16)
        tk.Button (actions, text = "Browse", command = self.browse_folder, bg = self.bg, fg = self.fg,
                   relief = "flat", font = ("Consolas", 11)).pack (side = "left")
        tk.Button (actions, text = "Apply", command = self.apply_settings, bg = self.bg, fg = self.fg,
                   relief = "flat", font = ("Consolas", 11)).pack (side = "right")

        self.results_frame = tk.Frame (self.root, bg = self.bg)
        self.results = tk.Text (self.results_frame, bg = self.bg, fg = self.fg, relief = "flat",
                                wrap = "word", insertbackground = self.fg, font = ("Consolas", 13))
        
        self.results.tag_configure ("title", foreground = self.fg, font = ("Consolas", 14, "bold"))
        self.results.tag_configure ("path", foreground = "#A0A0A0", font = ("Consolas", 12))
        self.results.tag_configure ("empty", foreground = "#FF4D4D", font = ("Consolas", 12, "bold"))
        self.scrollbar = tk.Scrollbar (self.results_frame, orient = "vertical")
        self.results.config (yscrollcommand = self.scrollbar.set)
        self.scrollbar.config (command = self.results.yview)
        self.results.pack (side = "left", fill = "both", expand = True)
        self.scrollbar.pack (side = "right", fill = "y")
        self.results_frame.place_forget ()

        self.root.bind ("<Return>", lambda _ : self.query ())
        self.root.bind ("<Configure>", lambda _ : self._layout ())
        self._layout ()

    def toggle_settings (self) -> None :
        if self.settings_panel.winfo_ismapped () :
            self.settings_panel.place_forget ()
        else :
            self.path_var.set (str (self.search_path))
            self.settings_panel.place (relx = 1.0, rely = 0.0, relwidth = 0.3, relheight = 1.0, anchor = "ne")
        self.settings.lift ()

    def browse_folder (self) -> None :
        chosen = filedialog.askdirectory ()
        if chosen :
            self.path_var.set (chosen)
            self.apply_settings ()

    def apply_settings (self) -> None :
        new_path = Path (self.path_var.get ()).expanduser ()
        if new_path.exists () and new_path.is_dir () :
            self.search_path = new_path
            self._save_path (new_path)
            self.index, self.doc_lens, self.N, self.avg_doc_len = None, None, None, None
            Thread (target = self._build_index, daemon = True).start ()
            self.toggle_settings ()

    def query (self) :
        query_str = self.search.get ()
        if self.index is None or self.doc_lens is None or self.N is None or self.avg_doc_len is None :
            self.results.config (state = "normal")
            self.results.delete ("1.0", tk.END)
            self.results.insert (tk.END, "Indexing... Please wait.", "empty")
            self.results.config (state = "disabled")
            return
        results = search (query_str, self.index, self.doc_lens, self.N, self.avg_doc_len)
        self.mode = "results"
        self.brand.config (text = "Indexor", font = ("Segoe UI", 20, "bold"))
        self._layout ()

        self.results.config (state = "normal")
        self.results.delete ("1.0", tk.END)
        if not results :
            self.results.insert (tk.END, "No results.", "empty")
            self.results.config (state = "disabled")
            return
        
        for i, (file, score) in enumerate (results) :
            if i > 0 :
                self.results.insert (tk.END, "\n\n")
            file_path = Path (file)
            title = file_path.stem.replace ("_", " ").strip ().title () or file_path.stem
            self.results.insert (tk.END, title + "\n", "title")
            self.results.insert (tk.END, str (file_path) + "  ", "path")
        self.results.config (state = "disabled")

    def _layout (self) :
        if self.mode == "home" :
            self.brand.place (relx = 0.5, rely = 0.4, anchor = "center")
            self.search_box.place (relx = 0.5, rely = 0.5, relwidth = 0.6, relheight = 0.06, anchor = "center")
            self.results_frame.place_forget ()
        else :
            self.brand.place (relx = 0.025, rely = 0.025, anchor = "nw")
            self.search_box.place (relx = 0.125, rely = 0.025, relwidth = 0.45, relheight = 0.06, 
                                   anchor = "nw")
            self.results_frame.place (relx = 0.05, rely = 0.12, relwidth = 0.9, relheight = 0.8)

    def mainloop (self) :
        self.root.mainloop ()

if __name__ == "__main__" :
    app = App ()
    app.mainloop ()

