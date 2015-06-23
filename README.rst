=================
python-anyconfig
=================

Overview
==========

.. image:: https://pypip.in/version/anyconfig/badge.svg
   :target: https://pypi.python.org/pypi/anyconfig/
   :alt: [Latest Version]

.. image:: https://pypip.in/py_versions/anyconfig/badge.svg
   :target: https://pypi.python.org/pypi/anyconfig/
   :alt: [Python versions]

.. .. image:: https://pypip.in/license/anyconfig/badge.png
   :target: https://pypi.python.org/pypi/anyconfig/
   :alt: MIT License

.. image:: https://api.travis-ci.org/ssato/python-anyconfig.png?branch=master
   :target: https://travis-ci.org/ssato/python-anyconfig
   :alt: [Test status]

.. image:: https://coveralls.io/repos/ssato/python-anyconfig/badge.png
   :target: https://coveralls.io/r/ssato/python-anyconfig
   :alt: [Coverage Status]

.. image:: https://landscape.io/github/ssato/python-anyconfig/master/landscape.png
   :target: https://landscape.io/github/ssato/python-anyconfig/master
   :alt: [Code Health]

.. image:: https://scrutinizer-ci.com/g/ssato/python-anyconfig/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/ssato/python-anyconfig
   :alt: [Code Quality]

.. image:: https://www.openhub.net/p/python-anyconfig/widgets/project_thin_badge.gif
   :target: https://www.openhub.net/p/python-anyconfig
   :alt: [Open HUB]

'anyconfig' [#]_ is a python library provides generic access to configuration
files in any formats (to be in the future) with configuration merge / cascade /
overlay and template config support.

* Author: Satoru SATOH <ssato@redhat.com>
* License: MIT

Current supported configuration file formats are:

* JSON with ``json`` or ``simplejson``
* YAML with ``PyYAML``
* Ini with ``configparser``
* ConifgObj with ``configobj``
* XML with ``lxml`` or ``ElementTree`` (experimental)
* Other formats some pluggale backends support (see the next sub section)

.. [#] This name took an example from the 'anydbm' python standard library.

Features
=========

- Provides very simple and unified APIs for various configuration files:

  - anyconfig.load() to load configuration files and it will return a dict-like object represents configuration loaded
  - anyconfig.loads() to load a configuration string and ...
  - anyconfig.dump() to dump a configuration file from a dict or dict-like object represents some configurations
  - anyconfig.dumps() to dump a configuration string from ...

- Can validate config files in any formats supported with JSON schema [#]_ in any formats supported and can represent the schema with jsonschema [#]_ 's help
- Can process jinja2-based template config files:

  - You can add include feature in config files for your applications with using jinja2's include directive

- Provides a CLI tool called anyconfig_cli to process configuration files:

  - Convert a/multiple configuration file[s] to another configuration files in different format
  - Get configuration value in a/multiple configuration file[s]

.. [#] http://json-schema.org
.. [#] https://pypi.python.org/pypi/jsonschema

Supported configuration formats
--------------------------------

anyconfig supports various configuration file formats if the required module is
available and the corresponding backend is ready:

.. csv-table::
   :header: "Format", "Type", "Required", "Notes"
   :widths: 10, 10, 30, 40

   JSON, json, ``json`` (standard lib) or ``simplejson`` [#]_, Enabled by default.
   Ini-like, ini, ``configparser`` (standard lib), Enabled by default.
   YAML, yaml, ``PyYAML`` [#]_, Enabled automatically if the requirement is satisfied.
   XML, xml, ``lxml`` [#]_ or ``ElementTree`` (experimental), Likewise.
   ConifgObj, configobj, ``configobj`` [#]_, Likewise.

You can check the supported formats (types) on your system by 'anyconfig_cli
-L' easily like this.

.. code-block:: console

  $ anyconfig_cli -L
  Supported config types: configobj, ini, json, xml, yaml
  $

And anyconfig utilizes plugin mechanism provided by setuptools [#]_ and
other formats may be supported by corresponding pluggale backends (see the next
sub section also) like Java properties format.

* Java properties file w/ pyjavaproperties [#]_ (experimental):

  * https://github.com/ssato/python-anyconfig-pyjavaproperties-backend

.. [#] https://pypi.python.org/pypi/simplejson
.. [#] https://pypi.python.org/pypi/PyYAML
.. [#] https://pypi.python.org/pypi/configobj
.. [#] https://pypi.python.org/pypi/lxml
.. [#] http://peak.telecommunity.com/DevCenter/setuptools#dynamic-discovery-of-services-and-plugins
.. [#] https://pypi.python.org/pypi/pyjavaproperties

Usage
======

see also: output of `python -c "import anyconfig; help(anyconfig)"`

anyconfig module
-------------------

Loading single config file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To load single config file:

.. code-block:: python

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

Also, you can pass backend (config loader) specific optional parameters to
these load and dump functions:

.. code-block:: python

  # from python -c "import json; help(json.load)":
  # Help on function load in module json:
  #
  # load(fp, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)
  #    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
  #    a JSON document) to a Python object.
  #    ...
  data5 = anyconfig.load("foo.json", parse_float=None)

.. note:: The returned object is an instance of
   anyconfig.mergeabledict.MergeableDict class by default, to support recursive
   merge operations needed when loading multiple config files.

Loading multiple config files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To load multiple config files:

.. code-block:: python

  import anyconfig

  # Specify config files by list of paths:
  data1 = anyconfig.load(["/etc/foo.d/a.json", "/etc/foo.d/b.json"])

  # Similar to the above but all or one of config files are missing:
  data2 = anyconfig.load(["/etc/foo.d/a.json", "/etc/foo.d/b.json"],
                         ignore_missing=True)

  # Specify config files by glob path pattern:
  data3 = anyconfig.load("/etc/foo.d/*.json")

  # Similar to the above, but parameters in the former config file will be simply
  # overwritten by the later ones:
  data4 = anyconfig.load("/etc/foo.d/*.json", merge=anyconfig.MS_REPLACE)

On loading multiple config files, you can choose 'strategy' to merge
configurations from the followings:

* anyconfig.MS_REPLACE: Replace all configuration parameter values provided in
  former config files are simply replaced w/ the ones in later config files.

  For example, if a.yml and b.yml are like followings:

  a.yml:


  .. code-block:: yaml

    a: 1
    b:
       - c: 0
       - c: 2
    d:
       e: "aaa"
       f: 3

  b.yml:

  .. code-block:: yaml

    b:
       - c: 3
    d:
       e: "bbb"

  then:

  .. code-block:: python

    load(["a.yml", "b.yml"], merge=anyconfig.MS_REPLACE)

  will give object such like:
  
  .. code-block:: python

    {'a': 1, 'b': [{'c': 3}], 'd': {'e': "bbb"}}

* anyconfig.MS_NO_REPLACE: Do not replace configuration parameter values
  provided in former config files.

  For example, if a.yml and b.yml are like followings:

  a.yml:
  
  .. code-block:: yaml

    b:
       - c: 0
       - c: 2
    d:
       e: "aaa"
       f: 3

  b.yml:
  
  .. code-block:: yaml

    a: 1
    b:
       - c: 3
    d:
       e: "bbb"

  then:
  
  .. code-block:: python

    load(["a.yml", "b.yml"], merge=anyconfig.MS_NO_REPLACE)

  will give object such like:

  .. code-block:: python

    {'a': 1, 'b': [{'c': 0}, {'c': 2}], 'd': {'e': "bbb", 'f': 3}}

* anyconfig.MS_DICTS (default): Merge dicts recursively. That is, the following:

  .. code-block:: python

    load(["a.yml", "b.yml"], merge=anyconfig.MS_DICTS)

  will give object such like:

  .. code-block:: python

    {'a': 1, 'b': [{'c': 3}], 'd': {'e': "bbb", 'f': 3}}

  This is the merge strategy choosen by default.

* anyconfig.MS_DICTS_AND_LISTS: Merge dicts and lists recursively. That is, the
  following:

  .. code-block:: python
 
    load(["a.yml", "b.yml"], merge=anyconfig.MS_DICTS_AND_LISTS)

  will give object such like:

  .. code-block:: python

    {'a': 1, 'b': [{'c': 0}, {'c': 2}, {'c': 3}], 'd': {'e': "bbb", 'f': 3}}

Validation
^^^^^^^^^^^^^

If you have jsonschema [#]_ installed, you can validate config files with using
anyconfig.validate() since 0.1.0.

.. code-block:: python

  # Validate a JSON config file (conf.json) with JSON schema (schema.json).
  # If validatation suceeds, `rc` -> True, `err` -> ''.
  conf1 = anyconfig.load("/path/to/conf.json")
  schema1 = anyconfig.load("/path/to/schema.json")
  (rc, err) = anyconfig.validate(conf1, schema1)

  # Similar to the above but both config and schema files are in YAML.
  conf2 = anyconfig.load("/path/to/conf.yml")
  schema2 = anyconfig.load("/path/to/schema.yml")
  (rc, err) = anyconfig.validate(conf2, schema2)

It's also possible to validate config files during load:

.. code-block:: python

  # Validate a config file (conf.yml) with JSON schema (schema.yml) while
  # loading the config file.
  conf1 = anyconfig.load("/a/b/c/conf.yml", ac_schema="/c/d/e/schema.yml")

  # Validate config loaded from multiple config files with JSON schema
  # (schema.json) while loading them.
  conf2 = anyconfig.load("conf.d/*.yml", ac_schema="/c/d/e/schema.json")

.. [#] https://pypi.python.org/pypi/jsonschema

Template config support
^^^^^^^^^^^^^^^^^^^^^^^^^^

Anyconfig module supports template config files since 0.0.6.
That is, config files written in Jinja2 template [#]_ will be compiled before
loading w/ backend module.

.. note:: Template config support is disabled by default to avoid side effects when processing config files of jinja2 template or having some expressions similar to jinaj2 template syntax.

Anyway, a picture is worth a thousand words. Here is an example of template
config files.

  .. code-block:: console

    ssato@localhost% cat a.yml
    a: 1
    b:
      {% for i in [1, 2, 3] -%}
      - index: {{ i }}
      {% endfor %}
    {% include "b.yml" %}
    ssato@localhost% cat b.yml
    c:
      d: "efg"
    ssato@localhost% anyconfig_cli a.yml --template -O yaml -s
    a: 1
    b:
    - {index: 1}
    - {index: 2}
    - {index: 3}
    c: {d: efg}
    ssato@localhost%

And another one:

  .. code-block:: console

    In [1]: import anyconfig

    In [2]: ls *.yml
    a.yml  b.yml

    In [3]: cat a.yml
    a: {{ a }}
    b:
      {% for i in b -%}
      - index: {{ i }}
      {% endfor %}
    {% include "b.yml" %}

    In [4]: cat b.yml
    c:
      d: "efg"

    In [5]: context = dict(a=1, b=[2, 4])

    In [6]: anyconfig.load("*.yml", ac_template=True, ac_context=context)
    Out[6]: {'a': 1, 'b': [{'index': 2}, {'index': 4}], 'c': {'d': 'efg'}}

.. [#] Jinja2 template engine (http://jinja.pocoo.org) and its language (http://jinja.pocoo.org/docs/dev/)

CLI frontend
---------------

There is a CLI frontend 'anyconfig_cli' to demonstrate the power of this library.

It can process various config files and output a merged config file:

.. code-block:: console

  ssato@localhost% anyconfig_cli -h
  Usage: anyconfig_cli [Options...] CONF_PATH_OR_PATTERN_0 [CONF_PATH_OR_PATTERN_1 ..]

  Examples:
    anyconfig_cli --list
    anyconfig_cli -I yaml -O yaml /etc/xyz/conf.d/a.conf
    anyconfig_cli -I yaml '/etc/xyz/conf.d/*.conf' -o xyz.conf --otype json
    anyconfig_cli '/etc/xyz/conf.d/*.json' -o xyz.yml \
      --atype json -A '{"obsoletes": "sysdata", "conflicts": "sysdata-old"}'
    anyconfig_cli '/etc/xyz/conf.d/*.json' -o xyz.yml \
      -A obsoletes:sysdata;conflicts:sysdata-old
    anyconfig_cli /etc/foo.json /etc/foo/conf.d/x.json /etc/foo/conf.d/y.json
    anyconfig_cli '/etc/foo.d/*.json' -M noreplace
    anyconfig_cli '/etc/foo.d/*.json' --get a.b.c
    anyconfig_cli '/etc/foo.d/*.json' --set a.b.c=1

  Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -L, --list            List supported config types
    -o OUTPUT, --output=OUTPUT
                          Output file path
    -I ITYPE, --itype=ITYPE
                          Select type of Input config files from ini, json, xml,
                          yaml [Automatically detected by file ext]
    -O OTYPE, --otype=OTYPE
                          Select type of Output config files from ini, json,
                          xml, yaml [Automatically detected by file ext]
    -M MERGE, --merge=MERGE
                          Select strategy to merge multiple configs from
                          replace, noreplace, merge_dicts, merge_dicts_and_lists
                          [merge_dicts]
    -A ARGS, --args=ARGS  Argument configs to override
    --atype=ATYPE         Explicitly select type of argument to provide configs
                          from ini, json, xml, yaml.  If this option is not set,
                          original parser is used: 'K:V' will become {K: V},
                          'K:V_0,V_1,..' will become {K: [V_0, V_1, ...]}, and
                          'K_0:V_0;K_1:V_1' will become {K_0: V_0, K_1: V_1}
                          (where the tyep of K is str, type of V is one of Int,
                          str, etc.
    --get=GET             Specify key path to get part of config, for example, '
                          --get a.b.c' to config {'a': {'b': {'c': 0, 'd': 1}}}
                          gives 0 and '--get a.b' to the same config gives {'c':
                          0, 'd': 1}.
    --set=SET             Specify key path to set (update) part of config, for
                          example, '--set a.b.c=1' to a config {'a': {'b': {'c':
                          0, 'd': 1}}} gives {'a': {'b': {'c': 1, 'd': 1}}}.
    -x, --ignore-missing  Ignore missing input files
    --template            Enable template config support
    --env                 Load configuration defaults from environment values
    -s, --silent          Silent or quiet mode
    -q, --quiet           Same as --silent option
    -v, --verbose         Verbose mode
  ssato@localhost%

Tips
======

Combination with other modules
--------------------------------

Anyconfig can be combined with other modules such as pyxdg and appdirs [#]_ .

For example, you can utilize anyconfig and pyxdg or appdirs in you application
software to load user config files like this:

.. code-block:: python

  import anyconfig
  import appdirs
  import os.path
  import xdg.BaseDirectory

  APP_NAME = "foo"
  APP_CONF_PATTERN = "*.yml"


  def config_path_by_xdg(app=APP_NAME, pattern=APP_CONF_PATTERN):
      return os.path.join(xdg.BaseDirectory.save_config_path(app), pattern)


  def config_path_by_appdirs(app=APP_NAME, pattern=APP_CONF_PATTERN):
      os.path.join(appdirs.user_config_dir(app), pattern)


  def load_config(fun=config_path_by_xdg):
      return anyconfig.load(fun())

.. [#] http://freedesktop.org/wiki/Software/pyxdg/
.. [#] https://pypi.python.org/pypi/appdirs/

Default config values
------------------------

Current implementation of anyconfig.\*load\*() do not provide a way to provide
some sane default configuration values (as a dict parameter for example)
before/while loading config files. Instead, you can accomplish that by a few
lines of code like the followings:

.. code-block:: python

   import anyconfig

   default = dict(foo=0, bar='1', baz=[2, 3])  # Default values
   conf = anyconfig.container(default)  # or: anyconfig.container(**default)
   conf_from_files = anyconfig.load("/path/to/config_files_dir/*.yml")

   conf.update(conf_from_files)

   # Use `conf` ... 

or:

.. code-block:: python

   default = dict(foo=0, bar='1', baz=[2, 3])
   conf = anyconfig.container(default)
   conf.update(anyconfig.load("/path/to/config_files_dir/*.yml"))

Environment Variables
------------------------

It's a piece of cake to use environment variables as config default values like
this:

.. code-block:: python

   conf = anyconfig.container(os.environ.copy())
   conf.update(anyconfig.load("/path/to/config_files_dir/*.yml"))

Convert from/to bunch objects
--------------------------------

It's easy to convert result conf object from/to bunch objects [#]_ as
anyconfig.load{s,} return a dict-like object:

.. code-block:: python

   import anyconfig
   import bunch

   conf = anyconfig.load("/path/to/some/config/files/*.yml")
   bconf = bunch.bunchify(conf)
   bconf.akey = ...  # Overwrite a config parameter.
      ...
   anyconfig.dump(bconf.toDict(), "/tmp/all.yml")

.. [#] bunch: https://pypi.python.org/pypi/bunch/

Build & Install
================

If you're Fedora or Red Hat Enterprise Linux user, you can install experimental
RPMs on http://copr.fedoraproject.org/coprs/ from:

* http://copr.fedoraproject.org/coprs/ssato/python-anyconfig/

or if you want to build yourself, then try:

.. code-block:: console

  $ python setup.py srpm && mock dist/SRPMS/python-anyconfig-<ver_dist>.src.rpm
  
or:

.. code-block:: console

  $ python setup.py rpm

and install built RPMs. 

Otherwise, try usual ways to build and/or install python modules such like 'pip
install anyconfig', 'easy_install anyconfig' and 'python setup.py bdist', etc.

How to hack
==============

How to write backend plugin modules
-------------------------------------

Backend class must inherit anyconfig.backend.Parser and need some member
variables and method ('load_impl' and 'dumps_impl' at minimum) implementations.

JSON and YAML backend modules (anyconfig.backend.{json,yaml}_) should be good
examples to write backend modules, I think.

Also, please take a look at some example backend plugin modules mentioned in
the `Supported configuration formats`_ section.

How to test
-------------

Try to run '[WITH_COVERAGE=1] ./pkg/runtest.sh [path_to_python_code]'.

TODO
======

* Make configuration (file) backends pluggable: Done

  * Remove some backends to support the following configuration formats:
  
    * Java properties file: Done
    * XML ?

* Allow users to select other containers for the tree of configuration objects
* Establish the way to test external backend modules

.. vim:sw=2:ts=2:et:
