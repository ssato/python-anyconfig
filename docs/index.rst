=================
python-anyconfig
=================

.. toctree::
    :maxdepth: 1

    usage
    api/index
    design
    cli

Introduction
=============

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

Also, anyconfig can process configuration files which are actually
`jinja2-based template <http://jinja.pocoo.org>`_ files:

- It's possible to prepare half-baked config files later rendered to.
- You can 'include' config files from config files for your applications with using jinja2's 'include' directive.

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

And anyconfig also can be used to validate configuration files in various
format with using JSON schema like the followings:

.. code-block:: python

  # Validate a JSON config file (conf.json) with JSON schema (schema.yaml).
  # If validatation suceeds, `rc` -> True, `err` -> ''.
  conf1 = anyconfig.load("/path/to/conf.json")
  schema1 = anyconfig.load("/path/to/schema.yaml")
  (rc, err) = anyconfig.validate(conf1, schema1)  # err should be empty if success (rc == 0)

  # Validate a config file (conf.yml) with JSON schema (schema.yml) while
  # loading the config file.
  conf2 = anyconfig.load("/a/b/c/conf.yml", ac_schema="/c/d/e/schema.yml")

  # Validate config loaded from multiple config files with JSON schema
  # (schema.json) while loading them.
  conf3 = anyconfig.load("conf.d/*.yml", ac_schema="/c/d/e/schema.json")

  # Generate jsonschema object from config files loaded.
  conf4 = anyconfig.load("conf.d/*.yml")
  scm4 = anyconfig.gen_schema(conf4)
  scm4_s = anyconfig.dumps(scm4, "json")

And in the last place, anyconfig provides a CLI tool called anyconfig_cli to
process configuration files:

- Convert a/multiple configuration file[s] to another configuration files in different formats
- Get configuration value in a/multiple configuration file[s]
- Validate configuration file[s] with JSON schema
- Generate JSON schema from given configuration file[s]

.. [#] This name took an example from the 'anydbm' python standard library.
.. [#] http://json-schema.org
.. [#] https://pypi.python.org/pypi/jsonschema

Supported configuration formats
--------------------------------

anyconfig supports various configuration file formats if the required module is
available and the corresponding backend is ready to use:

.. csv-table::
   :header: "Format", "Type", "Required", "Notes"
   :widths: 10, 10, 30, 40

   JSON, json, ``json`` (standard lib) or ``simplejson`` [#]_, Enabled by default.
   Ini-like, ini, ``configparser`` (standard lib), Enabled by default.
   YAML, yaml, ``PyYAML`` [#]_, Enabled automatically if the requirement is satisfied.
   XML, xml, ``lxml`` [#]_ or ``ElementTree`` (experimental), Likewise.
   ConifgObj, configobj, ``configobj`` [#]_, Likewise.
   MessagePack, msgpack, ``msgpack-python`` [#]_, Likewise.

You can check the supported formats (types) on your system by 'anyconfig_cli
-L' easily like this:

.. code-block:: console

  $ anyconfig_cli -L
  Supported config types: configobj, ini, json, xml, yaml
  $

or with the API 'anyconfig.list_types()':

.. code-block:: console

   In [8]: anyconfig.list_types()
   Out[8]: ['configobj', 'ini', 'json', 'xml', 'yaml']

   In [9]:

And anyconfig utilizes plugin mechanism provided by setuptools [#]_ and
other formats may be supported by corresponding pluggale backends (see the next
sub section also) like Java properties format.

* Java properties file w/ pyjavaproperties [#]_ (experimental):

  * https://github.com/ssato/python-anyconfig-pyjavaproperties-backend

.. [#] https://pypi.python.org/pypi/simplejson
.. [#] https://pypi.python.org/pypi/PyYAML
.. [#] https://pypi.python.org/pypi/lxml
.. [#] https://pypi.python.org/pypi/configobj
.. [#] https://pypi.python.org/pypi/msgpack-python
.. [#] http://peak.telecommunity.com/DevCenter/setuptools#dynamic-discovery-of-services-and-plugins
.. [#] https://pypi.python.org/pypi/pyjavaproperties

Installation
-------------

There is a couple of ways to install python-anyconfig:

- Binary RPMs:

  If you're Fedora or Red Hat Enterprise Linux user, you can install
  RPMs from the copr repository,
  http://copr.fedoraproject.org/coprs/ssato/python-anyconfig/.

- PyPI: You can install python-anyconfig from PyPI with using pip:

  .. code-block:: console

    $ pip install anyconfig

- Build RPMs from source: It's easy to build python-anyconfig with using rpm-build and mock:

  .. code-block:: console

    $ python setup.py srpm && mock dist/python-anyconfig-<ver_dist>.src.rpm

  or:

  .. code-block:: console

    $ python setup.py rpm

  and install built RPMs.

- Build from source: Of course you can build and/or install python modules in usual way such like 'python setup.py bdist', 'pip install git+https://github.com/ssato/python-anyconfig/' and so on.

Hack
=======

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

.. vim:sw=2:ts=2:et:
