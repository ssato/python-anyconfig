#
# pylint:disable=invalid-name
"""conf.py for sphinx."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve() / "src"))

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
]
source_suffix = ".rst"
master_doc = "index"

project = "python-anyconfig"
version = "3.13.11"
release = version

exclude_patterns = []

html_theme = "default"

autodoc_member_order = "bysource"
