"""setup.py to build package."""
import os
import pathlib
import re
import setuptools


# It might throw IndexError and so on.
VERSION = os.getenv("_PKG_VERSION", default="0.1.0")
VER_REG = re.compile(r"^__version__ = \"([^']+)\"")

for fpath in pathlib.Path("src").glob("**/__init__.py"):
    for line in fpath.open():
        match = VER_REG.match(line)
        if match:
            VERSION = match.groups()[0]
            break

setuptools.setup(
    version=VERSION,
    data_files=[("share/man/man1", ["docs/anyconfig_cli.1"])],
)
