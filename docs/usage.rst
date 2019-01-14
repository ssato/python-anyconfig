Usage
========

Here are some code examples of API usage.

Loading single config file
----------------------------

Here are some example code to load single config file:

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

  # Same as above as a result but make parser instance and pass it explicitly.
  yml_psr = anyconfig.find_loader(None, ac_parser="yaml")
  data6 = anyconfig.single_load(cnf_path, yml_psr)  # Or: anyconfig.load(...)

  # Similar to the previous examples but parser is specified explicitely to use
  # ruamel.yaml based YAML parser instead of PyYAML based one, and give
  # ruamel.yaml specific option.
  data7 = anyconfig.load(cnf_path, ac_parser="ruamel.yaml",
                         allow_duplicate_keys=True)

  # Same as above but open the config file explicitly before load.
  with anyconfig.open("/path/to/foo/conf.d/a.yml") as istrm:
      data10 = anyconfig.load(istrm)

  # Same as above but with specifying config type explicitly.
  with anyconfig.open("/path/to/foo/conf.d/a.yml", ac_parser="yaml") as istrm:
      data11 = anyconfig.load(istrm)

Exceptions raised on load
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Exception may be raised if something goes wrong. Then, you have to catch them
if you want to process more w/ errors ignored or handled.

.. code-block:: console

  >>> import anyconfig
  >>> anyconfig.single_load(None)
  Traceback (most recent call last):
    ...
  ValueError: path_or_stream or forced_type must be some value
  >>> anyconfig.single_load(None, ac_parser="backend_module_not_avail")
  Traceback (most recent call last):
    ...
  anyconfig.backends.UnknownParserTypeError: No parser found for type 'backend_module_not_avail'
  >>> anyconfig.single_load(None, ac_parser="not_existing_type")
  Traceback (most recent call last):
    ...
  anyconfig.backends.UnknownParserTypeError: No parser found for type 'not_existing_type'
  >>> anyconfig.single_load("unknown_type_file.conf")
  Traceback (most recent call last):
    ...
  anyconfig.backends.UnknownFileTypeError: No parser found for file 'unknown_type_file.conf'
  >>>

Common and backend specific Keyword options on load single config file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is a brief summary of keyword options prefixed with 'ac\_' to change the
behavior on load.

.. csv-table::
   :header: Option, Type, Note
   :widths: 10, 20, 40

   ac_parser, str or :class:`anyconfig.backend.base.Parser`, Forced parser type or parser object
   ac_dict, callable, "Any callable (function or class) to make mapping object will be returned as a result or None. If not given or ac_dict is None, default mapping object used to store resutls is dict or :class:`~collections.OrderedDict` if ac_ordered is True and selected backend can keep the order of items in mapping objects."
   ac_ordered, bool, True to keep resuls ordered. Please note that order of items in results may be lost depends on backend used.
   ac_template, bool, Assume given file may be a template file and try to compile it AAR if True
   ac_context, mapping object, Mapping object presents context to instantiate template
   ac_schema, str, JSON schema file path to validate given config file
   ac_query, str, JMESPath expression to query data

You can pass backend (config loader) specific keyword options to these load and
dump functions as needed along with the above anyconfig specific keyword
options:

.. code-block:: python

  # from python -c "import json; help(json.load)":
  # Help on function load in module json:
  #
  # load(fp, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)
  #    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
  #    a JSON document) to a Python object.
  #    ...
  data6 = anyconfig.load("foo.json", parse_float=None)

Allowed keyword options depend on backend, so please take a look at each
backend API docs for more details about it.

Others topics on load
^^^^^^^^^^^^^^^^^^^^^^^

Anyconfig also enables:

- to load a config which is actually a Jinja2 [#]_ template file, the file will be rendered before load. See `Template config support`_ section for more details.
- to validate a config file with a JSON schema [#]_ before load. See `Validation with and/or generate JSON Schema`_ section for more details.
- to search and filter results with a JMESPath expression [#]_ after load. See `Query results with JMESPath expression`_ section for more details.

.. note::
   The returned object is a mapping object, dict or collections.OrderedDict object by default.

.. [#] http://jinja.pocoo.org
.. [#] http://json-schema.org
.. [#] http://jmespath.org

Loading multiple config files
-------------------------------

Here are some example code to load multiple config files:

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

Strategies to merge data loaded from multiple config files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On loading multiple config files, you can choose 'strategy' to merge
configurations from the followings and pass it with ac_merge keyword option:

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

Or you you can implement custom function or class or anything callables to
merge nested dicts by yourself and utilize it with ac_merge keyword option like
this:

  .. code-block:: python

    def my_merge_fn(self, other, key, val=None, **options):
        """
        :param self: mapping object to update with `other`
        :param other: mapping object to update `self`
        :param key: key of mapping object to update
        :param val: value to update self alternatively

        :return: None but `self` will be updated
        """
        if key not in self:
            self[key] = other[key] if val is None else val

    load(["a.yml", "b.yml"], ac_merge=my_merge_fn)

Please refer to the exsiting functions in anyconfig.dicsts (_update_\*
functions) to implement custom functions to merge nested dicts for more
details.

Common and backend specific Keyword options on load multiple config files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is a brief summary of keyword options prefixed with 'ac\_' in addition to
the keyword options explained in the `Common and backend specific Keyword
options on load single config file`_  section to change the behavior on load
multiple files.

.. csv-table::
   :header: Option, Type, Note
   :widths: 10, 20, 40

   ac_merge, str, One of anyconfig.dicts.MERGE_STRATEGIES to select strategy of how to merge results loaded from multiple configuration files. See the doc of :mod:`anyconfig.dicts` for more details of strategies. The default is anyconfig.dicts.MS_DICTS.
   ac_marker, str, Glob marker string to detect paths patterns. '*' by default.

Dumping config data
---------------------

A pair of APIs are provided to dump config data loaded w/ using loading APIs as
described previously and corresponding to them.

- :func:`dumps`: Dump data as a string
- :func:`dump`: Dump data to file of which path was given or file-like object opened

.. note::

   To specify the format or backend type w/ ac_parser keyword option is
   necessary for :func:`dumps` API because anyconfig cannot determine the type
   w/o it.

Like loading APIs, you can pass common and backend specific keyword options to them.

- common keyword options: ac_parser to determine which backend to use
- backend specific keyword options: see each backends' details

Here are some examples of these usage:

.. code-block:: python

  In [1]: s = """a: A
     .....: b:
     .....:   - b0: 0
     .....:   - b1: 1
     .....: c:
     .....:   d:
     .....:     e: E
     .....: """

  In [2]: cnf = anyconfig.loads(s, ac_parser="yaml")

  In [3]: cnf
  Out[3]: {'a': 'A', 'b': [{'b0': 0}, {'b1': 1}], 'c': {'d': {'e': 'E'}}}

  In [4]: anyconfig.dumps(cnf, ac_parser="yaml")  # ac_parser option is necessary.
  Out[4]: 'a: A\nc:\n  d: {e: E}\nb:\n- {b0: 0}\n- {b1: 1}\n'

  In [5]: print(anyconfig.dumps(cnf, ac_parser="yaml"))
  a: A
  c:
    d: {e: E}
  b:
  - {b0: 0}
  - {b1: 1}

  In [6]: print(anyconfig.dumps(cnf, ac_parser="json"))
  {"a": "A", "c": {"d": {"e": "E"}}, "b": [{"b0": 0}, {"b1": 1}]}

  In [7]: print(anyconfig.dumps(cnf, ac_parser="ini"))  # It cannot!
  ---------------------------------------------------------------------------
  AttributeError                            Traceback (most recent call last)
  <ipython-input-228-2b2771a44a7e> in <module>()
  ----> 1 print(anyconfig.dumps(cnf, ac_parser="ini"))
      ...
  AttributeError: 'str' object has no attribute 'iteritems'

  In [8]: print(anyconfig.dumps(cnf, ac_parser="configobj"))
  a = A
  b = {'b0': 0}, {'b1': 1}
  [c]
  [[d]]
  e = E

  In [9]:

Like this example, it's not always possible to dump data to any formats because
of limitations of formarts and/or backends.

Keep the order of configuration items
----------------------------------------

If you want to keep the order of configuration items, specify ac_order=True on
load or specify ac_dict to any mapping object can save the order of items such
like :class:`collections.OrderedDict` (or
:class:`~anyconfig.compat.OrderedDict`). Otherwise, the order of configuration
items will be lost by default.

Please note that anyconfig.load APIs sometimes cannot keep the order of items
in the original data even if ac_order=True or ac_dict=<ordereddict> was
specified because used backend or module cannot keep that. For example, JSON
backend can keep items but current YAML backend does not due to the limitation
of YAML module it using.

Validation with and/or generate JSON Schema
----------------------------------------------

If jsonschema [#]_ is installed and available, you can validate config files
with using anyconfig.validate() since 0.0.10.

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

  # Similar to the above but exception will be raised if validation fails.
  (rc, _err) = anyconfig.validate(conf2, schema2, ac_schema_safe=False)

It's also able to validate config files during load:

.. code-block:: python

  # Validate a config file (conf.yml) with JSON schema (schema.yml) while
  # loading the config file.
  conf1 = anyconfig.load("/a/b/c/conf.yml", ac_schema="/c/d/e/schema.yml")

  # Validate config loaded from multiple config files with JSON schema
  # (schema.json) while loading them.
  conf2 = anyconfig.load("conf.d/*.yml", ac_schema="/c/d/e/schema.json")

And even if you don't have any JSON schema files, don't worry ;-), anyconfig
*can generate* the schema for your config files on demand and you can save it
in any formats anyconfig supports.

.. code-block:: python

  # Generate a simple JSON schema file from config file loaded.
  conf1 = anyconfig.load("/path/to/conf1.json")
  schema1 = anyconfig.gen_schema(conf1)
  anyconfig.dump(schema1, "/path/to/schema1.yml")

  # Generate more strict (precise) JSON schema file from config file loaded.
  schema2 = anyconfig.gen_schema(conf1, ac_schema_strict=True)
  anyconfig.dump(schema2, "/path/to/schema2.json")

.. note:: If you just want to generate JSON schema from your config files, then
   you don't need to install jsonschema in advance because *anyconfig can
   generate JSON schema without jsonschema module*.

.. [#] https://pypi.python.org/pypi/jsonschema

Template config support
---------------------------

anyconfig supports template config files since 0.0.6.  That is, config files
written in Jinja2 template [#]_ will be compiled before loading w/ backend
module.

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

Query results with JMESPath expression
-------------------------------------------

anyconfig supports to query result mapping object with JMESPath expression
since 0.8.3 like the following example [#]_ .

.. code-block:: console

  >>> yaml_s = """\
  ... locations:
  ...   - name: Seattle
  ...     state: WA
  ...   - name: New York
  ...     state: NY
  ...   - name: Olympia
  ...     state: WA
  ... """
  >>> query = "locations[?state == 'WA'].name | sort(@) | {WashingtonCities: join(', ', @)}"
  >>> anyconfig.loads(yaml_s, ac_parser="yaml", ac_query=query)
   {'WashingtonCities': 'Olympia, Seattle'}
  >>>

Different from other libraries can process JMESPath expressions, anyconfig can
query data of any formats it supports, with help of the jmespath support
library [#]_ . That is, you can query XML, YAML, BSON, Toml, and, of course
JSON files with JMESPath expression.

.. [#] This example is borrowed from JMESPath home, http://jmespath.org
.. [#] https://github.com/jmespath/jmespath.py

Other random topics with API usage
-----------------------------------

Suppress logging messages from anyconfig module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

anyconfig uses a global logger named **anyconfig** and logging messages are
suppressed by default as NullHandler was attached to the logger [#]_ . If you
want to see its log messages out, you have to configure it (add handler and
optionally set log level) like the followings.

- Set the log level and handler of anyconfig module before load to print log messages such as some backend modules are not available, when it's initialized:

.. code-block:: python

  In [1]: import logging

  In [2]: LOGGER = logging.getLogger("anyconfig")

  In [3]: LOGGER.addHandler(logging.StreamHandler())

  In [4]: LOGGER.setLevel(logging.ERROR)

  In [5]: import anyconfig

  In [6]: anyconfig.dumps(dict(a=1, b=[1,2]), "aaa")
  No parser found for given type: aaa
  Out[6]: '{"a": 1, "b": [1, 2]}'

  In [7]:

- Set log level of anyconfig module after load:

.. code-block:: console

  In [1]: import anyconfig, logging

  In [2]: LOGGER = logging.getLogger("anyconfig")

  In [3]: LOGGER.addHandler(logging.StreamHandler())

  In [4]: anyconfig.dumps(dict(a=2, b=[1,2]), "unknown_type")
  No parser found for given type: unknown_type
  Parser unknown_type was not found!
  Dump method not implemented. Fallback to json.Parser
  Out[4]: '{"a": 2, "b": [1, 2]}'

  In [5]:

.. [#] https://docs.python.org/2/howto/logging.html#library-config

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

   conf = dict(foo=0, bar='1', baz=[2, 3])  # Default values
   conf_from_files = anyconfig.load("/path/to/config_files_dir/*.yml")
   anyconfig.merge(conf, conf_from_files)  # conf will be updated.

   # Use `conf` ... 

or:

.. code-block:: python

   conf = dict(foo=0, bar='1', baz=[2, 3])
   anyconfig.merge(conf, anyconfig.load("/path/to/config_files_dir/*.yml"))

Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^

It's a piece of cake to use environment variables as config default values like
this:

.. code-block:: python

   conf = os.environ.copy()
   anyconfig.merge(conf, anyconfig.load("/path/to/config_files_dir/*.yml"))

Load from compressed files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since 0.2.0, python-anyconfig can load configuration from file or file-like
object, called *stream* internally. And this should help loading configurations
from compressed files.

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
