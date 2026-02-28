from rich.console import Console
from rich.theme import Theme

theme = Theme (
    {
        "info" : "bold cyan",
        "success" : "bold green",
        "warning" : "bold yellow",
        "error" : "bold red",
        "prompt" : "bold bright_white",
        "title" : "bold magenta",
        "result" : "white",
        "path" : "underline blue",
        "word" : "bold bright_cyan",
    }
)

console = Console (theme = theme)