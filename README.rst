=================
python-anyconfig
=================

.. image:: https://img.shields.io/pypi/v/anyconfig.svg
   :target: https://pypi.python.org/pypi/anyconfig/
   :alt: [Latest Version]

.. image:: https://img.shields.io/pypi/pyversions/anyconfig.svg
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

.. .. image:: https://www.openhub.net/p/python-anyconfig/widgets/project_thin_badge.gif
   :target: https://www.openhub.net/p/python-anyconfig
   :alt: [Open HUB]

Anyconfig [#]_ is a `MIT licensed <http://opensource.org/licenses/MIT>`_ python
library provides generic access to configuration files in various formats with
configuration merge / cascade / overlay and template config support.

Anyconfig provides very simple and unified APIs for various configuration
files:

- anyconfig.load() to load configuration files and it will return a dict-like object represents configuration loaded
- anyconfig.loads() to load a configuration string and ...
- anyconfig.dump() to dump a configuration file from a dict or dict-like object represents some configurations
- anyconfig.dumps() to dump a configuration string from ...
- anyconfig.validate() to validate configuration files with JSON schema [#]_ with a python module jsonschema's help [#]_ . Both configuration files and schema files can be written in any formats anyconfig supports.

Using anyconfig, you can load configuration files in various formats in the
same way, without taking care of each file format in some cases, like the
followings:

.. code-block:: python

  import anyconfig

  # Config type (format) is automatically detected by filename (file
  # extension) in some cases.
  conf1 = anyconfig.load("/path/to/foo/conf.d/a.yml")

  # Loaded config data is a dict-like object, for example:
  #
  #   conf1["a"] => 1
  #   conf1["b"]["b1"] => "xyz"
  #   conf1["c"]["c1"]["c13"] => [1, 2, 3]

  # Or you can specify the format (config type) explicitly if automatic
  # detection may not work.
  conf2 = anyconfig.load("/path/to/foo/conf.d/b.conf", "yaml")

  # Specify multiple config files by the list of paths. Configurations of each
  # files are merged.
  conf3 = anyconfig.load(["/etc/foo.d/a.json", "/etc/foo.d/b.json"])

  # Similar to the above but all or one of config file[s] is/are missing:
  conf4 = anyconfig.load(["/etc/foo.d/a.json", "/etc/foo.d/b.json"],
                         ignore_missing=True)

  # Specify config files by glob path pattern:
  conf5 = anyconfig.load("/etc/foo.d/*.json")

  # Similar to the above, but parameters in the former config file will be simply
  # overwritten by the later ones:
  conf6 = anyconfig.load("/etc/foo.d/*.json", merge=anyconfig.MS_REPLACE)

For more details of anyconfig, please take a look at the `documentation
<http://python-anyconfig.readthedocs.org/en/latest/>`_ is available on the Read
the Docs web site, which is also able to be built locally:

.. code-block:: console

   $ git clone https://github.com/ssato/python-anyconfig.git
   $ make -C python-anyconfig/docs

.. [#] This name took an example from the 'anydbm' python standard library.
.. [#] http://json-schema.org
.. [#] https://pypi.python.org/pypi/jsonschema

.. vim:sw=2:ts=2:et:
