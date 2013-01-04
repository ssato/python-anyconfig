"""Generic interface to loaders and parsers for various config file formats.

Instead of

    import json, yaml
    jd = json.load(open("foo.json"))
    yd = yaml.load(open("bar.yaml"))

use

    import anyconfig as ac
    jd = ac.load("foo.json")
    yd = ac.load("bar.yaml")

The returned object is an anyconfig.Bunch object, dict-like object but its
values are also accessible as attributes, by default.

"""
from .api import load, loads, mload, mload_metaconf, dump, dumps

VERSION = "0.0.3.2"

# If daily snapshot versioning mode:
#importt datetime
#VERSION = VERSION + datetime.datetime.now().strftime(".%Y%m%d")

__version__ = VERSION
__all__ = [
    "load", "loads", "mload", "mload_metaconf",
    "dump", "dumps",
]

__author__ = 'Satoru SATOH <ssat@redhat.com>'

# vim:sw=4:ts=4:et:
