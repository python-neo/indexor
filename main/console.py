"""
Shared Rich console theme and console instance for INDEXOR.
"""

from rich.console import Console
from rich.theme import Theme

theme = Theme (
    {
        "info" : "cyan",
        "success" : "green",
        "warning" : "yellow",
        "error" : "red",
        "prompt" : "bright_white",
        "title" : "magenta",
        "result" : "white",
        "path" : "underline blue",
        "word" : "bright_cyan",
    }
)

def get_console (no_colour : bool = False) -> Console :
    """
    Build a Rich console instance for INDEXOR.

    Parameters :
        no_colour (bool) : Disable terminal colours when `True`.

    Returns :
        Console : Configured Rich console.
    """
    return Console (theme = theme, no_color = no_colour)

console = get_console ()