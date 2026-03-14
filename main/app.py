import tkinter as tk

BG = "#000000"
FG = "#FFFFFF"
ACCENT = "#05EE67"
SOFT = "#0E0E0E"

class App :
    def __init__ (self) -> None :
        self.root = tk.Tk ()
        self.root.title ("Indexor")
        self.root.configure (bg = BG)
        self.root.state ("zoomed")

        self._build_ui ()

    def _build_ui (self) -> None :
        canvas = tk.Canvas (self.root, bg = BG, highlightthickness = 0)
        canvas.pack (fill = "both", expand = True)

        title = tk.Label (canvas, text = "I N D E X O R", bg = BG, fg = ACCENT, font = ("Segoe UI", 32, "bold"))

        title_window = canvas.create_window (0, 0, window = title, anchor = "center")

        entry = tk.Entry (
            canvas,
            bg = SOFT,
            fg = FG,
            insertbackground = FG,
            relief = "flat",
            font = ("Segoe UI", 14)
        )
        entry_window = canvas.create_window (0, 0, window = entry, anchor = "center")

        def layout (_event = None) -> None :
            w = canvas.winfo_width ()
            h = canvas.winfo_height ()
            canvas.coords (title_window, w / 2, h / 2 - 120)
            bar_w = min (680, int (w * 0.7))
            canvas.coords (entry_window, w / 2, h / 2)
            entry.configure (width = int (bar_w / 12))

        self.root.bind ("<Configure>", layout)

def main () -> None :
    app = App ()
    app.root.mainloop ()

if __name__ == "__main__" :
    main ()
