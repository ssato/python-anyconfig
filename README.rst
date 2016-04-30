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

.. .. image:: https://api.travis-ci.org/ssato/python-anyconfig.png?branch=master

.. image:: https://img.shields.io/travis/ssato/python-anyconfig.svg
   :target: https://travis-ci.org/ssato/python-anyconfig
   :alt: [Test status]

.. .. image:: https://coveralls.io/repos/ssato/python-anyconfig/badge.png

.. image:: https://img.shields.io/coveralls/ssato/python-anyconfig.svg
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

.. image:: https://readthedocs.org/projects/python-anyconfig/badge/?version=latest
   :target: http://python-anyconfig.readthedocs.io/en/latest/?badge=latest
   :alt: [Doc Status]


Introduction
=============

python-anyconfig [#]_ is a `MIT licensed <http://opensource.org/licenses/MIT>`_
python library provides common APIs to access to configuration files in various
formats with some useful features such as contents merge, templates and schema
validation/generation support.

- Home: https://github.com/ssato/python-anyconfig
- (Latest) Doc: http://python-anyconfig.readthedocs.org/en/latest/
- PyPI: https://pypi.python.org/pypi/anyconfig
- Copr RPM repos: https://copr.fedoraproject.org/coprs/ssato/python-anyconfig/

I, Satoru SATOH <ssato@redhat.com>, developed and keep maintain this library
with others' help (see AUTHORS.txt for more details).

.. [#] This name took an example from the 'anydbm' python standard library.

Features
----------

python-anyconfig provides very simple and unified APIs to process configuration
files in various formats:

- Loading configuration files:

  - anyconfig.load() loads configuration files or file/file-like objects and return a dict-like object represents loaded configuration
  - anyconfig.loads() loads configuration from a string just like json.loads does

- Dumping configuration files:

  - anyconfig.dump() dumps a configuration file from a dict or dict-like object represents configuration
  - anyconfig.dumps() dumps a configuration string from a dict or dict-like object represents configuration

- Schema validation and generation of configuration files:

  - anyconfig.validate() validates configuration loaded with anyconfig.load() with JSON schema [#]_ (object) also loaded with anyconfig.load(). anyconfig.load() may help loading JSON schema file[s] in any formats anyconfig supports.
  - anyconfig.gen_schema() generates a minimum JSON schema object to validate given configuration file[s] later.

It enables to load configuration file[s] in various formats in the same manner,
and in some cases, even there is no need to take care of the actual format of
configuration file[s] like the followings:

.. code-block:: python

  import anyconfig

  # Config type (format) is automatically detected by filename (file
  # extension) in some cases.
  conf1 = anyconfig.load("/path/to/foo/conf.d/a.yml")

  # Similar to the above but load from file object opened:
  with open("/path/to/foo/conf.d/a.yml") as fileobj:
      conf1_1 = anyconfig.load(fileobj)

  # Loaded config data is a dict-like object, for example:
  #
  #   conf1["a"] => 1
  #   conf1["b"]["b1"] => "xyz"
  #   conf1["c"]["c1"]["c13"] => [1, 2, 3]

  # Or you can specify the format (config type) explicitly if automatic
  # detection may not work.
  conf2 = anyconfig.load("/path/to/foo/conf.d/b.conf", ac_parser="yaml")

  # Likewise.
  with open("/path/to/foo/conf.d/b.conf") as fileobj:
      conf2_2 = anyconfig.load(fileobj, ac_parser="yaml")

  # Specify multiple config files by the list of paths. Configurations of each
  # files are merged.
  conf3 = anyconfig.load(["/etc/foo.d/a.json", "/etc/foo.d/b.json"])

  # Similar to the above but all or one of config file[s] is/are missing:
  conf4 = anyconfig.load(["/etc/foo.d/a.json", "/etc/foo.d/b.json"],
                         ignore_missing=True)

  # Specify config files by glob path pattern:
  conf5 = anyconfig.load("/etc/foo.d/*.json")

  # Similar to the above, but parameters in the former config file will be simply
  # overwritten by the later ones instead of merge:
  conf6 = anyconfig.load("/etc/foo.d/*.json", ac_merge=anyconfig.MS_REPLACE)

Also, it can process configuration files which are actually
`jinja2-based template <http://jinja.pocoo.org>`_ files:

- Enables to load a substantial configuration rendered from half-baked configuration template files with given context
- Enables to load a series of configuration files indirectly 'include'-d from a/some configuration file[s] with using jinja2's 'include' directive.

.. code-block:: console

  In [1]: import anyconfig

  In [2]: open("/tmp/a.yml", 'w').write("a: {{ a|default('aaa') }}\n")

  In [3]: anyconfig.load("/tmp/a.yml", ac_template=True)
  Out[3]: {'a': 'aaa'}

  In [4]: anyconfig.load("/tmp/a.yml", ac_template=True, ac_context=dict(a='bbb'))
  Out[4]: {'a': 'bbb'}

  In [5]: open("/tmp/b.yml", 'w').write("{% include 'a.yml' %}\n")  # 'include'

  In [6]: anyconfig.load("/tmp/b.yml", ac_template=True, ac_context=dict(a='ccc'))
  Out[6]: {'a': 'ccc'}

And python-anyconfig enables to validate configuration files in various format
with using JSON schema like the followings:

.. code-block:: python

  # Validate a JSON config file (conf.json) with JSON schema (schema.yaml).
  # If validatation suceeds, `rc` -> True, `err` -> ''.
  conf1 = anyconfig.load("/path/to/conf.json")
  schema1 = anyconfig.load("/path/to/schema.yaml")
  (rc, err) = anyconfig.validate(conf1, schema1)  # err is empty if success, rc == 0

  # Validate a config file (conf.yml) with JSON schema (schema.yml) while
  # loading the config file.
  conf2 = anyconfig.load("/a/b/c/conf.yml", ac_schema="/c/d/e/schema.yml")

  # Validate config loaded from multiple config files with JSON schema
  # (schema.json) while loading them.
  conf3 = anyconfig.load("conf.d/*.yml", ac_schema="/c/d/e/schema.json")

  # Generate jsonschema object from config files loaded and get string
  # representation.
  conf4 = anyconfig.load("conf.d/*.yml")
  scm4 = anyconfig.gen_schema(conf4)
  scm4_s = anyconfig.dumps(scm4, "json")

And in the last place, python-anyconfig provides a CLI tool called
anyconfig_cli to process configuration files and:

- Convert a/multiple configuration file[s] to another configuration files in different format
- Get configuration value in a/multiple configuration file[s]
- Validate configuration file[s] with JSON schema
- Generate minimum JSON schema file to validate given configuration file[s]

.. [#] http://json-schema.org

Supported configuration formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

python-anyconfig supports various (configuration) file formats if the required
module is available and the corresponding backend is ready to use:

.. csv-table:: Supported formats
   :header: "Format", "Type", "Requirement", "Notes"
   :widths: 10, 10, 30, 40

   JSON, json, ``json`` (standard lib) or ``simplejson`` [#]_, Enabled by default.
   Ini-like, ini, ``configparser`` (standard lib), Ditto.
   Java properties [#]_ , properties, None (native implementation with standard lib), Ditto.
   XML, xml, ``lxml`` [#]_ or ``ElementTree``, Ditto.
   YAML, yaml, ``PyYAML`` [#]_, Enabled automatically if the left requirement is satisfied.
   ConifgObj, configobj, ``configobj`` [#]_, Ditto.
   MessagePack, msgpack, ``msgpack-python`` [#]_, Ditto.
   TOML, toml, ``toml`` [#]_, Ditto.
   BSON, bson, bson in ``pymongo`` [#]_, Ditto.

The supported formats of python-anyconfig on your system is able to be listed
by 'anyconfig_cli -L' like this:

.. code-block:: console

  $ anyconfig_cli -L
  Supported config types: bson, configobj, ini, json, msgpack, toml, xml, yaml
  $

or with the API 'anyconfig.list_types()' will show them: 

.. code-block:: console

   In [8]: anyconfig.list_types()
   Out[8]: ['bson', 'configobj', 'ini', 'json', 'msgpack', 'toml', 'xml', 'yaml']

   In [9]:

It utilizes plugin mechanism provided by setuptools [#]_ and other formats may
be supported by corresponding pluggale backends like the following:

- Java properties backend utilizes pyjavaproperties [#]_ (just an example implementation):

  - https://github.com/ssato/python-anyconfig-pyjavaproperties-backend

.. [#] https://pypi.python.org/pypi/simplejson
.. [#] ex. https://docs.oracle.com/javase/7/docs/api/java/util/Properties.html
.. [#] https://pypi.python.org/pypi/PyYAML
.. [#] https://pypi.python.org/pypi/lxml
.. [#] https://pypi.python.org/pypi/configobj
.. [#] https://pypi.python.org/pypi/msgpack-python
.. [#] https://pypi.python.org/pypi/toml
.. [#] https://pypi.python.org/pypi/pymongo
.. [#] http://peak.telecommunity.com/DevCenter/setuptools#dynamic-discovery-of-services-and-plugins
.. [#] https://pypi.python.org/pypi/pyjavaproperties

Installation
-------------

Requirements
^^^^^^^^^^^^^^

Many runtime dependencies are resolved dynamically and python-anyconfig just
disables specific features if required dependencies are not satisfied.
Therefore, only python standard library is required to install and use
python-anyconfig at minimum.

The following packages need to be installed along with python-anycofig to
enable the features.

.. csv-table::
   :header: "Feature", "Requirements", "Notes"
   :widths: 20, 10, 25

   YAML load/dump, PyYAML, none
   ConifgObj load/dump, configobj, none
   MessagePack load/dump, msgpack-python, none
   TOML load/dump, toml, none
   BSON load/dump, bson, bson from pymongo package may work and bson [#]_ does not
   Template config, Jinja2 [#]_ , none
   Validation with JSON schema, jsonschema [#]_ , Not required to generate JSON schema.

.. [#] https://pypi.python.org/pypi/bson/
.. [#] https://pypi.python.org/pypi/Jinja2/
.. [#] https://pypi.python.org/pypi/jsonschema/

How to install
^^^^^^^^^^^^^^^^

There is a couple of ways to install python-anyconfig:

- Binary RPMs:

  If you're Fedora or Red Hat Enterprise Linux user, you can install RPMs from
  the copr repository,
  http://copr.fedoraproject.org/coprs/ssato/python-anyconfig/.

  If what you're running is Fedora, maybe you can enable this repo with DNF's
  copr plugin's help [#]_ like this:

  .. code-block:: console

    # dnf copr enable ssato/python-anyconfig

- PyPI: You can install python-anyconfig from PyPI with using pip:

  .. code-block:: console

    $ pip install anyconfig

- pip from git repo:

  .. code-block:: console

     $ pip install git+https://github.com/ssato/python-anyconfig/

- Build RPMs from source: It's easy to build python-anyconfig with using rpm-build and mock:

  .. code-block:: console

    $ python setup.py srpm && mock dist/python-anyconfig-<ver_dist>.src.rpm

  or:

  .. code-block:: console

    $ python setup.py rpm

  and install built RPMs.

- Build from source: Of course you can build and/or install python modules in usual way such like 'python setup.py bdist', 'pip install git+https://github.com/ssato/python-anyconfig/' and so on.

.. [#] http://dnf-plugins-core.readthedocs.org/en/latest/copr.html

Help and feedbak
-----------------

If you have any issues / feature request / bug reports with python-anyconfig,
please open an issue ticket on github.com
(https://github.com/ssato/python-anyconfig/issues).

The following areas are still insufficient, I think.

- Make python-anyconfig robust for invalid inputs
- Make python-anyconfig scaled: some functions are limited by max recursion depth.
- Documentation:

  - Especially API docs need more fixes and enhancements! CLI doc is non-fulfilling also.
  - English is not my native lang and there are many wrong and hard-to-understand expressions.

Any feedbacks, helps, suggestions are welcome! Please open github issues for
these kind of problems also!

.. vim:sw=2:ts=2:et:
