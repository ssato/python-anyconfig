=================
python-anyconfig
=================

Generic access to configuration files in any formats (to be in the future).

* Author: Satoru SATOH <ssato@redhat.com>
* License: MIT

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

  # Same as above
  data2 = anyconfig.single_load("/path/to/foo/conf.d/a.yml")

  # Or you can specify config type explicitly.
  data3 = anyconfg.load("/path/to/foo/conf.d/b.conf", "yaml")

  # Same as above
  data4 = anyconfig.single_load("/path/to/foo/conf.d/b.conf", "yaml")


To load multiple config files::

  import anyconfig

  # Specify config files by list of paths:
  data1 = anyconfig.load(["/etc/foo.d/a.json", "/etc/foo.d/b.json"])

  # Specify config files by glob path pattern:
  data2 = anyconfig.load("/etc/foo.d/*.json")

  # Similar to above, but parameters in the former config file will be simply
  # overwritten by the later ones:
  data3 = anyconfig.load("/etc/foo.d/*.json", merge=anyconfig.MS_REPLACE)

CUI frontend
-------------

There is a CUI frontend 'anyconfig_cui' for demonstration purpose.

It can process various config files and output a summarized config file::

  $ anyconfig_cui -h
  Usage: anyconfg_cui [Options...] CONF_PATH_OR_PATTERN_0 [CONF_PATH_OR_PATTERN_1 ..]

  Examples:
    anyconfg_cui --list
    anyconfg_cui -I yaml /etc/xyz/conf.d/a.conf
    anyconfg_cui -I yaml '/etc/xyz/conf.d/*.conf' -o xyz.conf --otype json
    anyconfg_cui /etc/foo.json /etc/foo/conf.d/x.json /etc/foo/conf.d/y.json


  Options:
    -h, --help            show this help message and exit
    -D, --debug           Debug mode
    -L, --list            List supported config types
    -o OUTPUT, --output=OUTPUT
                          Output file path
    -I ITYPE, --itype=ITYPE
                          Explicitly select type of Input config files from ini,
                          json, yaml, xml, properties [Automatically detected by
                          file path]
    -O OTYPE, --otype=OTYPE
                          Explicitly select type of Output config files from
                          ini, json, yaml, xml, properties [Automatically
                          detected by file path]
  $


Test Status
=============

.. image:: https://api.travis-ci.org/ssato/python-anyconfig.png?branch=master
   :target: https://travis-ci.org/ssato/python-anyconfig
   :alt: Test status

.. vim:sw=2:ts=2:et:
