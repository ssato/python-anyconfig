"""Generic interface to loaders and parsers for various config file formats.

Instead of

    import json, yaml
    jd = json.load(open("foo.json"))
    yd = yaml.load(open("bar.yaml"))

use

    import anyconfig
    jd = anyconfig.load("foo.json")
    yd = anyconfig.load("bar.yaml")

The returned object is an instance of anyconfig.mergeabledict.MergeableDict
class, dict-based class support recursive dicts and lists merge operation.

You can also load multiple config files at once w/ anyconfig.multi_load:

    conf = anyconfig.multi_load(["foo.json", "bar.yaml"])

or if path of config files can be specified w/ a glob pattern, you can use
anyconfig.load instead such like:

    conf = anyconfig.load("/etc/xyz/conf.d/*.conf", "yaml")

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

    load(["a.yml", "b.yml"], merge=anyconfig.MS_REPLACE)

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

    load(["a.yml", "b.yml"], merge=anyconfig.MS_NO_REPLACE)

  will give object such like::

    {'a': 1, 'b': [{'c': 0}, {'c': 2}], 'd': {'e': "bbb", 'f': 3}}

* anyconfig.MS_DICTS: Merge dicts recursively. That is, the following

  ::

    load(["a.yml", "b.yml"], merge=anyconfig.MS_DICTS)

  will give object such like::

    {'a': 1, 'b': [{'c': 3}], 'd': {'e': "bbb", 'f': 3}}

* anyconfig.MS_DICTS_AND_LISTS: Merge dicts and lists recursively. That is, the
  following::

    load(["a.yml", "b.yml"], merge=anyconfig.MS_DICTS_AND_LISTS)

  will give object such like::

    {'a': 1, 'b': [{'c': 0}, {'c': 2}, {'c': 3}], 'd': {'e': "bbb", 'f': 3}}

"""
from .api import single_load, multi_load, load, loads, dump, dumps, \
    list_types, find_parser, \
    MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS

VERSION = "0.0.3.6"

# If daily snapshot versioning mode:
#import datetime
#VERSION = VERSION + datetime.datetime.now().strftime(".%Y%m%d")

__version__ = VERSION
__all__ = [
    "list_types", "find_parser",
    "single_load", "multi_load", "load", "loads",
    "dump", "dumps", "list_types",
    "MS_REPLACE", "MS_NO_REPLACE", "MS_DICTS", "MS_DICTS_AND_LISTS",
]

__author__ = 'Satoru SATOH <ssat@redhat.com>'

# vim:sw=4:ts=4:et:
