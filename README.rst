=================
python-anyconfig
=================

Generic access to configuration files in any formats (to be in the future) with
configuration merge (or cascade, overlay) support.

* Author: Satoru SATOH <ssato@redhat.com>
* License: MIT

Current supported configuration file formats are:

* JSON w/ json or simplejson
* YAML w/ PyYAML
* Ini w/ configparser
* XML w/ lxml or ElementTree (experimental)
* Java properties file w/ pyjavaproperties (experimental):

  * With backend plugin: https://github.com/ssato/python-anyconfig-pyjavaproperties-backend

* Ini file like format configobj supports (experimental):

  * With backend plugin: https://github.com/ssato/python-anyconfig-configobj-backend

Usage
======

see also: output of `python -c "import anyconfig; help(anyconfig)"`

anyconfig module
-------------------

To load single config file::

  import anyconfig

  # Config type (format) is automatically detected by filename (file
  # extension).
  data1 = anyconfig.load("/path/to/foo/conf.d/a.yml")

  # Loaded config data is a dict-like object.
  # examples:
  # data1["a"] => 1
  # data1["b"]["b1"] => "xyz"
  # data1["c"]["c1"]["c13"] => [1, 2, 3]

  # Same as above
  data2 = anyconfig.single_load("/path/to/foo/conf.d/a.yml")

  # Or you can specify config type explicitly.
  data3 = anyconfig.load("/path/to/foo/conf.d/b.conf", "yaml")

  # Same as above
  data4 = anyconfig.single_load("/path/to/foo/conf.d/b.conf", "yaml")

It's possible to pass config loader specific option parameter to load and dump::

  # from python -c "import json; help(json.load)":
  # Help on function load in module json:
  #
  # load(fp, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)
  #    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
  #    a JSON document) to a Python object.
  #    ...
  data5 = anyconfig.load("foo.json", parse_float=None)

.. note::

   The returned object is an instance of anyconfig.mergeabledict.MergeableDict
   class by default to support recursive merge operations needed when loading
   multiple config files.

To load multiple config files::

  import anyconfig

  # Specify config files by list of paths:
  data1 = anyconfig.load(["/etc/foo.d/a.json", "/etc/foo.d/b.json"])

  # Specify config files by glob path pattern:
  data2 = anyconfig.load("/etc/foo.d/*.json")

  # Similar to above, but parameters in the former config file will be simply
  # overwritten by the later ones:
  data3 = anyconfig.load("/etc/foo.d/*.json", merge=anyconfig.MS_REPLACE)

On loading multiple config files, you can choose strategy to merge configs from
the followings:

* anyconfig.MS_REPLACE: Replace all configuration parameters provided in former
  config files are simply replaced w/ the ones in later config files.

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

* anyconfig.MS_DICTS: Merge dicts recursively. That is, the following::

    load(["a.yml", "b.yml"], merge=anyconfig.MS_DICTS)

  will give object such like::

    {'a': 1, 'b': [{'c': 3}], 'd': {'e': "bbb", 'f': 3}}

* anyconfig.MS_DICTS_AND_LISTS: Merge dicts and lists recursively. That is, the
  following::

    load(["a.yml", "b.yml"], merge=anyconfig.MS_DICTS_AND_LISTS)

  will give object such like::

    {'a': 1, 'b': [{'c': 0}, {'c': 2}, {'c': 3}], 'd': {'e': "bbb", 'f': 3}}


CLI frontend
-------------

There is a CLI frontend 'anyconfig_cli' for its demonstration purpose.

It can process various config files and output a merged config file::

  $ anyconfig_cli -h
  Usage: anyconfig_cli [Options...] CONF_PATH_OR_PATTERN_0 [CONF_PATH_OR_PATTERN_1 ..]

  Examples:
    anyconfig_cli --list
    anyconfig_cli -I yaml /etc/xyz/conf.d/a.conf
    anyconfig_cli -I yaml '/etc/xyz/conf.d/*.conf' -o xyz.conf --otype json
    anyconfig_cli '/etc/xyz/conf.d/*.json' -o xyz.yml \
      --atype json -A '{"obsoletes": "sysdata", "conflicts": "sysdata-old"}'
    anyconfig_cli '/etc/xyz/conf.d/*.json' -o xyz.yml \
      -A obsoletes:sysdata;conflicts:sysdata-old
    anyconfig_cli /etc/foo.json /etc/foo/conf.d/x.json /etc/foo/conf.d/y.json
    anyconfig_cli '/etc/foo.d/*.json' -M noreplace


  Options:
    -h, --help            show this help message and exit
    -L, --list            List supported config types
    -o OUTPUT, --output=OUTPUT
                          Output file path
    -I ITYPE, --itype=ITYPE
                          Select type of Input config files from ini, json,
                          yaml, xml [Automatically detected by file ext]
    -O OTYPE, --otype=OTYPE
                          Select type of Output config files from ini, json,
                          yaml, xml [Automatically detected by file ext]
    -M MERGE, --merge=MERGE
                          Select strategy to merge multiple configs from
                          noreplace, merge_dicts_and_lists, merge_dicts, replace
                          [merge_dicts]
    -A ARGS, --args=ARGS  Argument configs to override
    --atype=ATYPE         Explicitly select type of argument config from ini,
                          json, yaml, xml. If this option is not set, original
                          parser is used:  'K:V' will become {K: V},
                          'K:V_0,V_1,..' will become {K: [V_0, V_1, ...]}, and
                          'K_0:V_0;K_1:V_1' will become {K_0: V_0, K_1: V_1}
                          (where the tyep of K is str, type of V is one of Int,
                          str, etc.
    -s, --silent          Silent or quiet mode
    -q, --quiet           Same as --silent option
    -v, --verbose         Verbose mode
  $


Build & Install
================

If you're Fedora or Red Hat Enterprise Linux user, try::

  $ python setup.py srpm && mock dist/SRPMS/python-anyconfig-<ver_dist>.src.rpm
  
or::

  $ python setup.py rpm

and install built RPMs. 

Otherwise, try usual ways to build and/or install python modules such like
'easy_install anyconfig', 'python setup.py bdist', etc.

Test Status
=============

.. image:: https://api.travis-ci.org/ssato/python-anyconfig.png?branch=master
   :target: https://travis-ci.org/ssato/python-anyconfig
   :alt: Test status

TODO
======

* Make configuration (file) backend pluggable: Done

  * use setuptools. ref. http://bit.ly/Y5ngrM
  * Remove some backends support less major config formats:
  
    * Java properties file
    * XML ?

* Allow users to select other containers for the tree of configuration objects
* Implement the standard way to test external backend modules

.. vim:sw=2:ts=2:et:
