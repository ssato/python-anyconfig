"""
.. module:: anyconfig
   :platform: Unix, Windows
   :synopsis: Generic interface to loaders for various config file formats.

Instead of::

    import json, yaml
    jd = json.load(open("foo.json"))
    yd = yaml.load(open("bar.yaml"))
        ...
    json.dump(open("foo-new.json", w))
    yaml.dump(open("bar-new.yaml", w))

you can write like the following::

    import anyconfig
    jd = anyconfig.load("foo.json")
    yd = anyconfig.load("bar.yaml")
        ...
    anyconfig.dump(open("foo-new.json", w))
    anyconfig.dump(open("bar-new.yaml", w))

.. note::

   It's possible to pass config loader specific option parameter to load and
   dump methods for each type of Parser,

   ex. anyconfig.load("foo.json", parse_float=None)

You can also load multiple config files at once w/ anyconfig.multi_load or
anyconfig.load (the later one does not distinguish between single and multiple
config files)::

    conf = anyconfig.multi_load(["foo.json", "bar.yaml"])

or if path of config files can be specified w/ a glob pattern, you can use
anyconfig.load instead such like::

    conf = anyconfig.load("/etc/xyz/conf.d/*.conf", "yaml")

The returned object is an instance of anyconfig.mergeabledict.MergeableDict
class by default to support recursive merge operations needed when loading
multiple config files.

On loading multiple config files, you can choose strategy to merge configs from
the followings:

* anyconfig.MS_REPLACE: Replace all configuration parameters provided in former
  config files w/ the ones in later config files.

  For example, if a.yml and b.yml are like followings:

  a.yml::

    a: 1
    b:
       - c: 0
       - c: 2
    d:
       e: "aaa"
       f: 3

  b.yml::

    b:
       - c: 3
    d:
       e: "bbb"

  then::

    load(["a.yml", "b.yml"], ac_merge=anyconfig.MS_REPLACE)

  will give object such like::

    {'a': 1, 'b': [{'c': 3}], 'd': {'e': "bbb"}}

* anyconfig.MS_NO_REPLACE: Do not replace configuration parameters provided in
  former config files.

  For example, if a.yml and b.yml are like followings:

  a.yml::

    b:
       - c: 0
       - c: 2
    d:
       e: "aaa"
       f: 3

  b.yml::

    a: 1
    b:
       - c: 3
    d:
       e: "bbb"

  then::

    load(["a.yml", "b.yml"], ac_merge=anyconfig.MS_NO_REPLACE)

  will give object such like::

    {'a': 1, 'b': [{'c': 0}, {'c': 2}], 'd': {'e': "bbb", 'f': 3}}

* anyconfig.MS_DICTS (default): Merge dicts recursively. That is, the following

  ::

    load(["a.yml", "b.yml"], ac_merge=anyconfig.MS_DICTS)

  will give object such like::

    {'a': 1, 'b': [{'c': 3}], 'd': {'e': "bbb", 'f': 3}}

  This is the merge strategy choosen by default.

* anyconfig.MS_DICTS_AND_LISTS: Merge dicts and lists recursively. That is, the
  following::

    load(["a.yml", "b.yml"], ac_merge=anyconfig.MS_DICTS_AND_LISTS)

  will give object such like::

    {'a': 1, 'b': [{'c': 0}, {'c': 2}, {'c': 3}], 'd': {'e': "bbb", 'f': 3}}

"""
from .globals import AUTHOR, VERSION
from .api import (
    single_load, multi_load, load, loads, dump, dumps, validate, gen_schema,
    list_types, find_loader, to_container, set_loglevel, get, set_,
    MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS
)

__author__ = AUTHOR
__version__ = VERSION

__all__ = [
    "single_load", "multi_load", "load", "loads", "dump", "dumps", "validate",
    "gen_schema", "list_types", "find_loader", "to_container",
    "set_loglevel", "get", "set_",
    "MS_REPLACE", "MS_NO_REPLACE", "MS_DICTS", "MS_DICTS_AND_LISTS",
]

# vim:sw=4:ts=4:et:
