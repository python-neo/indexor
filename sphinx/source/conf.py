import sys
import os

project = 'Indexor'
copyright = '2026, Aarav Agarwal'
author = 'Aarav Agarwal'
version = '0.5.1'
release = '0.5.1'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon"
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = "furo"
html_static_path = []
html_theme_options = {
    "light_css_variables" : {},
    "dark_css_variables" : {},
    "sidebar_hide_name" : False,
    "navigation_with_keys": True,
}
html_dark_mode = True

sys.path.insert (0, os.path.abspath ("../../"))
