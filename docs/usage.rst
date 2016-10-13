API Usage
==========

Here are some code examples of API usage.

Loading single config file
----------------------------

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

  # Same as above but I recommend to use the former.
  data2 = anyconfig.single_load("/path/to/foo/conf.d/a.yml")

  # Or you can specify config type explicitly as needed.
  cnf_path = "/path/to/foo/conf.d/b.conf"
  data3 = anyconfig.load(cnf_path, ac_parser="yaml")

  # Same as above but ...
  data4 = anyconfig.single_load(cnf_path, ac_parser="yaml")

  # Same as above as a result but make parser instance and pass it explicitly.
  yml_psr = anyconfig.find_loader(None, ac_parser="yaml")
  data5 = anyconfig.single_load(cnf_path, yml_psr)  # Or: anyconfig.load(...)

You can pass backend (config loader) specific optional parameters to
these load and dump functions as needed:

.. code-block:: python

  # from python -c "import json; help(json.load)":
  # Help on function load in module json:
  #
  # load(fp, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)
  #    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
  #    a JSON document) to a Python object.
  #    ...
  data6 = anyconfig.load("foo.json", parse_float=None)

Also it's possible:

- to load a config which is actually a Jinja2 [#]_ template file, the file will be rendered before load. See `Template config support`_ section for more details.
- to validate a config file with a JSON schema [#]_ before load. See `Validation with JSON Schema`_ section for more details.

.. note:: The returned object is an instance of m9dicts.UpdateWithMergeDict
   class by default, to support recursive merge operations needed when loading
   multiple config files.

.. [#] http://jinja.pocoo.org
.. [#] http://json-schema.org

Loading multiple config files
-------------------------------

To load multiple config files:

.. code-block:: python

  import anyconfig

  # Specify config files by list of paths:
  data1 = anyconfig.load(["/etc/foo.d/a.json", "/etc/foo.d/b.json"])

  # Similar to the above but all or one of config files are missing:
  data2 = anyconfig.load(["/etc/foo.d/a.json", "/etc/foo.d/b.json"],
                         ignore_missing=True)

  # Specify config files by glob path pattern:
  cnf_path = "/etc/foo.d/*.json"
  data3 = anyconfig.load(cnf_path)

  # Similar to above but make parser instance and pass it explicitly.
  psr = anyconfig.find_loader(cnf_path)
  data4 = anyconfig.load(cnf_path, psr)

  # Similar to the above but parameters in the former config file will be simply
  # overwritten by the later ones:
  data5 = anyconfig.load("/etc/foo.d/*.json", ac_merge=anyconfig.MS_REPLACE)

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

    load(["a.yml", "b.yml"], ac_merge=anyconfig.MS_REPLACE)

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

    load(["a.yml", "b.yml"], ac_merge=anyconfig.MS_NO_REPLACE)

  will give object such like:

  .. code-block:: python

    {'a': 1, 'b': [{'c': 0}, {'c': 2}], 'd': {'e': "bbb", 'f': 3}}

* anyconfig.MS_DICTS (default): Merge dicts recursively. That is, the following:

  .. code-block:: python

    load(["a.yml", "b.yml"], ac_merge=anyconfig.MS_DICTS)

  will give object such like:

  .. code-block:: python

    {'a': 1, 'b': [{'c': 3}], 'd': {'e': "bbb", 'f': 3}}

  This is the merge strategy choosen by default.

* anyconfig.MS_DICTS_AND_LISTS: Merge dicts and lists recursively. That is, the
  following:

  .. code-block:: python
 
    load(["a.yml", "b.yml"], ac_merge=anyconfig.MS_DICTS_AND_LISTS)

  will give object such like:

  .. code-block:: python

    {'a': 1, 'b': [{'c': 0}, {'c': 2}, {'c': 3}], 'd': {'e': "bbb", 'f': 3}}

Keep the order of configuration items
----------------------------------------

If you want to keep the order of configuration items, specify ac_order=True on
load. Otherwise, the order of configuration items will be lost by default.
But please note that it's not true that any backend can keep the order of keys.
For example, JSON backend can do that but current YAML backend does not.

Validation with JSON Schema
-------------------------------

If you have jsonschema [#]_ installed, you can validate config files with using
anyconfig.validate() since 0.0.10.

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
---------------------------

anyconfig module supports template config files since 0.0.6.
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

Other random topics with API usage
-----------------------------------

Suppress logging messages from anyconfig module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

anyconfig uses a global logger named 'anyconfig' [#]_ and provide an utility
function :func:`anyconfig.set_loglevel` to set logging level of this logger
like the followings:

- Set log level of anyconfig module before load:

.. code-block:: python

  import logging

  logging.getLogger("anyconfig").setLevel(logging.ERROR)

  import anyconfig

  ...

- Set log level of anyconfig module after load:

.. code-block:: python

  import anyconfig
  import logging

  anyconfig.set_loglevel(logging.WARN)  # Or: anyconfig.LOGGER.setLevel(logging.ERROR)

.. [#] I https://docs.python.org/2/howto/logging.html#library-config

Combination with other modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

anyconfig can be combined with other modules such as pyxdg and appdirs [#]_ .

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Current implementation of anyconfig.\*load\*() do not provide a way to provide
some sane default configuration values (as a dict parameter for example)
before/while loading config files. Instead, you can accomplish that by a few
lines of code like the followings:

.. code-block:: python

   import anyconfig

   default = dict(foo=0, bar='1', baz=[2, 3])  # Default values
   conf = anyconfig.to_container(default)  # or: anyconfig.to_container(**default)
   conf_from_files = anyconfig.load("/path/to/config_files_dir/*.yml")

   conf.update(conf_from_files)

   # Use `conf` ... 

or:

.. code-block:: python

   default = dict(foo=0, bar='1', baz=[2, 3])
   conf = anyconfig.to_container(default)
   conf.update(anyconfig.load("/path/to/config_files_dir/*.yml"))

Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^

It's a piece of cake to use environment variables as config default values like
this:

.. code-block:: python

   conf = anyconfig.to_container(os.environ.copy())
   conf.update(anyconfig.load("/path/to/config_files_dir/*.yml"))

Load from compressed files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since 0.2.0, python-anyconfig can load configuration from file or file-like
object (called 'stream' internally). And this should help loading
configurations from compressed files.

- Loading from a compressed JSON config file:

.. code-block:: python

   import gzip

   strm = gzip.open("/path/to/gzip/compressed/cnf.json.gz")
   cnf = anyconfig.load(strm, "json")

- Loading from some compressed JSON config files:

.. code-block:: python

   import gzip
   import glob

   cnfs = "/path/to/gzip/conf/files/*.yml.gz"
   strms = [gzip.open(f) for f in sorted(glob.glob(cnfs))]
   cnf = anyconfig.load(strms, "yaml")

Please note that "json" argument passed to anyconfig.load is necessary to help
anyconfig find out the configuration type of the file.

Convert from/to bunch objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

.. vim:sw=2:ts=2:et:
