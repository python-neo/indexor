import tkinter as tk
from .indexer import build_index
from pathlib import Path
from .search import search

search_path = Path ().home () / "Desktop"

class App :
    def __init__ (self) -> None :
        self.bg = "#000000"
        self.fg = "#29C611"
        self.root = tk.Tk ()
        self.root.title ("Indexor")
        self.root.state ("zoomed")
        self.root.config (bg = self.bg)
        self.index, self.doc_lens, self.N, self.avg_doc_len = build_index (str (search_path))
        self.mode = "home"
        self.home_screen ()

    def home_screen (self) :
        self.search_box = tk.Frame (self.root, width = 700, height = 40, bg = self.bg, 
                                    highlightbackground = self.fg, highlightthickness = 2, 
                                    highlightcolor = self.fg)
        self.search_box.place (relx = 0.5, rely = 0.5, relwidth = 0.6, relheight = 0.06, anchor = "center")
        self.search_box.pack_propagate (False)

        self.search = tk.Entry (self.search_box, fg = self.fg, insertbackground = self.fg, 
                                relief = "flat", bg = self.bg, font = ("Cambria Code", 12))
        self.search.pack (fill = "both", padx = 3, pady = 8)

        self.brand = tk.Label (self.root, bg = self.bg, fg = self.fg, text = "I n d e x o r", 
                               font = ("Segoe UI", 40, "bold"))
        self.brand.place (relx = 0.5, rely = 0.4, anchor = "center")

        self.results_frame = tk.Frame (self.root, bg = self.bg)
        self.results = tk.Text (self.results_frame, bg = self.bg, fg = self.fg, relief = "flat", 
                                wrap = "word", insertbackground = self.fg)
        self.results.tag_configure ("title", foreground = self.fg)
        self.results.tag_configure ("path", foreground = "#9BEF6E")
        self.results.tag_configure ("score", foreground = "#BFBFBF")
        self.results.tag_configure ("empty", foreground = "#FF6666")
        self.results.pack (fill = "both", expand = True)
        self.results_frame.place_forget ()

        self.root.bind ("<Return>", lambda _ : self.query ())
        self.root.bind ("<Configure>", lambda _ : self._layout ())
        self._layout ()

    def query (self) :
        query_str = self.search.get ()
        results = search (query_str, self.index, self.doc_lens, self.N, self.avg_doc_len)
        self.mode = "results"
        self.brand.config (text = "Indexor", font = ("Segoe UI", 20, "bold"))
        self._layout ()

        self.results.config (state = "normal")
        self.results.delete ("1.0", tk.END)
        if not results :
            self.results.insert (tk.END, "No results.", "empty")
            return
        
        for i, (file, score) in enumerate (results) :
            if i > 0 :
                self.results.insert (tk.END, "\n\n")
            file_path = Path (file)
            title = file_path.stem.replace ("_", " ").strip ().title () or file_path.stem
            self.results.insert (tk.END, title + "\n", "title")
            self.results.insert (tk.END, str (file_path) + "  ", "path")
            self.results.insert (tk.END, f"({score:.4f})", "score")
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
