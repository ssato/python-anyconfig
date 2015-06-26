CLI Usage
===========

python-anyconfig contains a CLI frontend 'anyconfig_cli' to demonstrate the
power of this library.

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
    -S SCHEMA, --schema=SCHEMA
                          Specify Schema file[s] path
    -V, --validate        Only validate input files and do not output. You must
                          specify schema file with -S/--schema option.
    -s, --silent          Silent or quiet mode
    -q, --quiet           Same as --silent option
    -v, --verbose         Verbose mode
  ssato@localhost%

.. vim:sw=2:ts=2:et:
