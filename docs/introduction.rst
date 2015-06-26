Introduction
=============

anyconfig [#]_ is a python library provides generic access to configuration
files in any formats (to be in the future) with configuration merge / cascade /
overlay and template config support.

- Author: Satoru SATOH <ssato@redhat.com>
- License: MIT

.. [#] This name took an example from the 'anydbm' python standard library.

Basic features
----------------

anyconfig provides very simple and unified APIs for various configuration files:

- anyconfig.load() to load configuration files and it will return a dict-like object represents configuration loaded
- anyconfig.loads() to load a configuration string and ...
- anyconfig.dump() to dump a configuration file from a dict or dict-like object represents some configurations
- anyconfig.dumps() to dump a configuration string from ...
- anyconfig.validate() to validate configuration files with JSON schema [#]_ with a python module jsonschema's help [#]_ . Both configuration files and schema files can be written in any formats anyconfig supports.

anyconfig can process jinja2-based template config files:

- It's possible to prepare half-baked config files later rendered to.
- You can add include feature in config files for your applications with using jinja2's include directive

anyconfig provides a CLI tool called anyconfig_cli to process configuration files:

- Convert a/multiple configuration file[s] to another configuration files in different format
- Get configuration value in a/multiple configuration file[s]
- Validate configuration file[s] with JSON shcmea

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

Installation
-------------

There is a couple of ways to install python-anyconfig:

- Binary RPMs:

  If you're Fedora or Red Hat Enterprise Linux user, you can install
  experimental RPMs on http://copr.fedoraproject.org/coprs/ from:

  - http://copr.fedoraproject.org/coprs/ssato/python-anyconfig/

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

.. vim:sw=2:ts=2:et:
