CLI Usage
===========

python-anyconfig contains a CLI frontend 'anyconfig_cli' to demonstrate the
power of this library.

It can process config files in any formats supported in your environment and:

- output merged/converted config outputs w/ modifications needed
- output schema file for given inputs
- merge/convert input config and extract part of the config

.. code-block:: console

  ssato@localhost% anyconfig_cli -h
  Usage: anyconfig_cli [Options...] CONF_PATH_OR_PATTERN_0 [CONF_PATH_OR_PATTERN_1 ..]

  Examples:
    anyconfig_cli --list  # -> Supported config types: configobj, ini, json, ...
    # Merge and/or convert input config to output config [file]
    anyconfig_cli -I yaml -O yaml /etc/xyz/conf.d/a.conf
    anyconfig_cli -I yaml '/etc/xyz/conf.d/*.conf' -o xyz.conf --otype json
    anyconfig_cli '/etc/xyz/conf.d/*.json' -o xyz.yml \
      --atype json -A '{"obsoletes": "sysdata", "conflicts": "sysdata-old"}'
    anyconfig_cli '/etc/xyz/conf.d/*.json' -o xyz.yml \
      -A obsoletes:sysdata;conflicts:sysdata-old
    anyconfig_cli /etc/foo.json /etc/foo/conf.d/x.json /etc/foo/conf.d/y.json
    anyconfig_cli '/etc/foo.d/*.json' -M noreplace
    # Get/set part of input config
    anyconfig_cli '/etc/foo.d/*.json' --get a.b.c
    anyconfig_cli '/etc/foo.d/*.json' --set a.b.c=1

  Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -o OUTPUT, --output=OUTPUT
                          Output file path
    -I ITYPE, --itype=ITYPE
                          Select type of Input config files from configobj, ini,
                          json, msgpack, xml, yaml [Automatically detected by
                          file ext]
    -O OTYPE, --otype=OTYPE
                          Select type of Output config files from configobj,
                          ini, json, msgpack, xml, yaml [Automatically detected
                          by file ext]
    -M MERGE, --merge=MERGE
                          Select strategy to merge multiple configs from
                          replace, noreplace, merge_dicts, merge_dicts_and_lists
                          [merge_dicts]
    -A ARGS, --args=ARGS  Argument configs to override
    --atype=ATYPE         Explicitly select type of argument to provide configs
                          from configobj, ini, json, msgpack, xml, yaml.  If
                          this option is not set, original parser is used: 'K:V'
                          will become {K: V}, 'K:V_0,V_1,..' will become {K:
                          [V_0, V_1, ...]}, and 'K_0:V_0;K_1:V_1' will become
                          {K_0: V_0, K_1: V_1} (where the tyep of K is str, type
                          of V is one of Int, str, etc.
    -x, --ignore-missing  Ignore missing input files
    -T, --template        Enable template config support
    -E, --env             Load configuration defaults from environment values
    -S SCHEMA, --schema=SCHEMA
                          Specify Schema file[s] path
    -s, --silent          Silent or quiet mode
    -q, --quiet           Same as --silent option
    -v, --verbose         Verbose mode

    List specific options:
      -L, --list          List supported config types

    Schema specific options:
      --validate          Only validate input files and do not output. You must
                          specify schema file with -S/--schema option.
      --gen-schema        Generate JSON schema for givne config file[s] and
                          output it instead of (merged) configuration.

    Get/set options:
      -Q QUERY, --query=QUERY
                          Query with JMESPath expression language. See
                          http://jmespath.org for more about JMESPath
                          expression. This option is not used with --get option
                          at the same time. Please note that python module to
                          support JMESPath expression
                          (https://pypi.python.org/pypi/jmespath/) is required
                          to use this option
      --get=GET           Specify key path to get part of config, for example, '
                          --get a.b.c' to config {'a': {'b': {'c': 0, 'd': 1}}}
                          gives 0 and '--get a.b' to the same config gives {'c':
                          0, 'd': 1}.
      --set=SET           Specify key path to set (update) part of config, for
                          example, '--set a.b.c=1' to a config {'a': {'b': {'c':
                          0, 'd': 1}}} gives {'a': {'b': {'c': 1, 'd': 1}}}.
  ssato@localhost%

List supported config types (formats)
---------------------------------------

anyconfig_cli lists config types (formats) supported in your environment with -L/--list option:

.. code-block:: console

  $ anyconfig_cli -L
  Supported config types: configobj, ini, json, msgpack, xml, yaml
  $ anyconfig_cli --list
  Supported config types: configobj, ini, json, msgpack, xml, yaml
  $

Merge and/or convert input config
-----------------------------------

anyconfig_cli can process a config file or config files and output merged
config in various formats it can support in your environment.

Here are some such examples.

- single input config file, input type is automatically detected from the input file's extension:

.. code-block:: console

  $ cat /tmp/a.yml
  a: 1
  b:
    c:
      - aaa
      - bbb
  d:
    e:
      f: xyz
      g: true
  $ anyconfig_cli -O json /tmp/a.yml
  Loading: /tmp/a.yml
  {"a": 1, "b": {"c": ["aaa", "bbb"]}, "d": {"e": {"g": true, "f": "xyz"}}}

- single input config file with the input type and output option:

.. code-block:: console

  $ diff -u /tmp/a.{yml,conf}
  $ anyconfig_cli -I yaml -O configobj /tmp/a.conf -o /tmp/a.ini --silent
  $ cat /tmp/a.ini
  a = 1
  [b]
  c = aaa, bbb
  [d]
  [[e]]
  g = True
  f = xyz
  $

- multiple input config files:

.. code-block:: console

  $ cat /tmp/b.yml
  b:
    i:
      j: 123
  d:
    e:
      g: hello, world
  l: -1
  $ anyconfig_cli /tmp/{a,b}.yml --silent
  a: 1
  b:
    c: [aaa, bbb]
    i: {j: 123}
  d:
    e: {f: xyz, g: 'hello, world'}
  l: -1

  $

- multiple input config files with merge strategy option:

.. code-block:: console

  $ anyconfig_cli /tmp/{a,b}.yml -M replace --silent
  a: 1
  b:
    i: {j: 123}
  d:
    e: {g: 'hello, world'}
  l: -1

  $

- multiple input config files with template option:

.. code-block:: console

  $ cat /tmp/c.yml
  m: {{ d.e.g }}
  n: {{ b.i.j }}
  $ anyconfig_cli /tmp/{a,b,c}.yml --silent --template
  a: 1
  b:
    c: [aaa, bbb]
    i: {j: 123}
  d:
    e: {f: xyz, g: 'hello, world'}
  l: -1
  m: hello, world
  n: 123

  $ ls /tmp/*.yml
  /tmp/a.yml  /tmp/b.yml  /tmp/c.yml
  $ # Same as the privious one but inputs are given in a glob pattern.
  $ anyconfig_cli '/tmp/*.yml' --silent --template  # same as the privious one
  a: 1
  b:
    c: [aaa, bbb]
    i: {j: 123}
  d:
    e: {f: xyz, g: 'hello, world'}
  l: -1
  m: hello, world
  n: 123

  $

- Missing input config files:

.. code-block:: console

  $ ls /tmp/not-exist-file.yml
  ls: cannot access /tmp/not-exist-file.yml: No such file or directory
  $ anyconfig_cli --ignore-missing /tmp/not-exist-file.yml -s
  {}

  $ anyconfig_cli --ignore-missing /tmp/not-exist-file.yml -s -A "a: aaa"
  No config type was given. Try to parse...
  {a: aaa}

  $ anyconfig_cli --ignore-missing /tmp/not-exist-file.yml -s -A "a: aaa; b: 123"
  No config type was given. Try to parse...
  {a: aaa, b: 123}

  $

Schema generation and validation
----------------------------------

anyconfig_cli can process input config file[s] and generate JSON schema file to
validate the config like this:

- An usage example of schema generation option --gen-schema of anyconfig_cli:

.. code-block:: console

  $ cat /tmp/a.yml
  a: 1
  b:
    c:
      - aaa
      - bbb
  d:
    e:
      f: xyz
      g: true
  $ anyconfig_cli --gen-schema /tmp/a.yml -s -o /tmp/a.schema.json
  $ jq '.' /tmp/a.schema.json
  {
    "properties": {
      "d": {
        "properties": {
          "e": {
            "properties": {
              "f": {
                "type": "string"
              },
              "g": {
                "type": "boolean"
              }
            },
            "type": "object"
          }
        },
        "type": "object"
      },
      "b": {
        "properties": {
          "c": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "type": "object"
      },
      "a": {
        "type": "integer"
      }
    },
    "type": "object"
  }
  $

- and schema validation option --validate (and --schema) of anyconfig_cli:

.. code-block:: console

  $ anyconfig_cli -A 'a: aaa' --atype yaml /tmp/a.yml -o /tmp/a2.yml --silent
  $ head -n 1 /tmp/a.yml
  a: 1
  $ head -n 1 /tmp/a2.yml
  a: aaa
  $ anyconfig_cli --validate --schema /tmp/a.schema.json /tmp/a.yml
  Loading: /tmp/a.schema.json
  Loading: /tmp/a.yml
  Validation succeeds
  $ anyconfig_cli --validate --schema /tmp/a.schema.json /tmp/a.yml -s; echo $?
  0
  $ anyconfig_cli --validate --schema /tmp/a.schema.json /tmp/a2.yml -s; echo $?
  'aaa' is not of type u'integer'

  Failed validating u'type' in schema[u'properties'][u'a']:
      {u'type': u'integer'}

  On instance[u'a']:
      'aaa'
  Validation failed1
  $

Query/Get/set - extract or set part of input config
------------------------------------------------------

Here is usage examples of --get option of anyconfig_cli:

.. code-block:: console

  $ cat /tmp/a.yml
  a: 1
  b:
    c:
      - aaa
      - bbb
  d:
    e:
      f: xyz
      g: true
  $ anyconfig_cli /tmp/a.yml --get d.e.f --silent
  xyz
  $ anyconfig_cli /tmp/a.yml --get b.c --silent
  ['aaa', 'bbb']
  $ anyconfig_cli /tmp/a.yml --query d.e.g --silent
  True
  $ anyconfig_cli /tmp/a.yml --query 'b.c[::-1]' --silent
  ['bbb', 'aaa']

and an usage example of --set option of anyconfig_cli with same input:

.. code-block:: console

  $ anyconfig_cli /tmp/a.yml --set "d.e.g=1000" --set "b.c=ccc," --silent
  a: 1
  b:
    c: [ccc]
  d:
    e: {f: xyz, g: true}

  $

.. vim:sw=2:ts=2:et:
