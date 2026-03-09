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

console = Console (theme = theme)
