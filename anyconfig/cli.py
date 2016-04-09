#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""CLI frontend module for anyconfig.
"""
from __future__ import absolute_import, print_function

import codecs
import locale
import logging
import optparse
import os
import sys

import anyconfig.api as API
import anyconfig.compat
import anyconfig.globals
import anyconfig.mdicts
import anyconfig.parser


_ENCODING = locale.getdefaultlocale()[1]
API.LOGGER.addHandler(logging.StreamHandler())

if anyconfig.compat.IS_PYTHON_3:
    import io

    _ENCODING = _ENCODING.lower()

    # TODO: What should be done for an error, "AttributeError: '_io.StringIO'
    # object has no attribute 'buffer'"?
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=_ENCODING)
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding=_ENCODING)
    except AttributeError:
        pass
else:
    sys.stdout = codecs.getwriter(_ENCODING)(sys.stdout)
    sys.stderr = codecs.getwriter(_ENCODING)(sys.stderr)

USAGE = """\
%prog [Options...] CONF_PATH_OR_PATTERN_0 [CONF_PATH_OR_PATTERN_1 ..]

Examples:
  %prog --list  # -> Supported config types: configobj, ini, json, ...
  # Merge and/or convert input config to output config [file]
  %prog -I yaml -O yaml /etc/xyz/conf.d/a.conf
  %prog -I yaml '/etc/xyz/conf.d/*.conf' -o xyz.conf --otype json
  %prog '/etc/xyz/conf.d/*.json' -o xyz.yml \\
    --atype json -A '{"obsoletes": "syscnf", "conflicts": "syscnf-old"}'
  %prog '/etc/xyz/conf.d/*.json' -o xyz.yml \\
    -A obsoletes:syscnf;conflicts:syscnf-old
  %prog /etc/foo.json /etc/foo/conf.d/x.json /etc/foo/conf.d/y.json
  %prog '/etc/foo.d/*.json' -M noreplace
  # Get/set part of input config
  %prog '/etc/foo.d/*.json' --get a.b.c
  %prog '/etc/foo.d/*.json' --set a.b.c=1
  # Validate with JSON schema or generate JSON schema:
  %prog --validate -S foo.conf.schema.yml '/etc/foo.d/*.xml'
  %prog --gen-schema '/etc/foo.d/*.xml' -o foo.conf.schema.yml"""

DEFAULTS = dict(loglevel=1, list=False, output=None, itype=None,
                otype=None, atype=None, merge=API.MS_DICTS,
                ignore_missing=False, template=False, env=False,
                schema=None, validate=False, gen_schema=False)


def to_log_level(level):
    """
    :param level: Logging level in int = 0 .. 2

    >>> to_log_level(0) == logging.WARN
    True
    >>> to_log_level(5)  # doctest: +IGNORE_EXCEPTION_DETAIL, +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: wrong log level passed: 5
    >>>
    """
    if not (level >= 0 and level < 3):
        raise ValueError("wrong log level passed: " + str(level))

    return [logging.WARN, logging.INFO, logging.DEBUG][level]


_ATYPE_HELP_FMT = """\
Explicitly select type of argument to provide configs from %s.

If this option is not set, original parser is used: 'K:V' will become {K: V},
'K:V_0,V_1,..' will become {K: [V_0, V_1, ...]}, and 'K_0:V_0;K_1:V_1' will
become {K_0: V_0, K_1: V_1} (where the tyep of K is str, type of V is one of
Int, str, etc."""

_GET_HELP = ("Specify key path to get part of config, for example, "
             "'--get a.b.c' to config {'a': {'b': {'c': 0, 'd': 1}}} "
             "gives 0 and '--get a.b' to the same config gives "
             "{'c': 0, 'd': 1}. Path expression can be JSON Pointer "
             "expression (http://tools.ietf.org/html/rfc6901) such like "
             "'', '/a~1b', '/m~0n'.")
_SET_HELP = ("Specify key path to set (update) part of config, for "
             "example, '--set a.b.c=1' to a config {'a': {'b': {'c': 0, "
             "'d': 1}}} gives {'a': {'b': {'c': 1, 'd': 1}}}.")


def parse_args(argv=None, defaults=None):
    """
    Make up an option and arguments parser.

    :param defaults: Default option values
    """
    if defaults is None:
        defaults = DEFAULTS

    ctypes = API.list_types()
    ctypes_s = ", ".join(ctypes)
    type_help = "Select type of %s config files from " + \
        ctypes_s + " [Automatically detected by file ext]"

    mts = API.MERGE_STRATEGIES
    mts_s = ", ".join(mts)
    mt_help = "Select strategy to merge multiple configs from " + \
        mts_s + " [%(merge)s]" % defaults

    parser = optparse.OptionParser(USAGE, version="%%prog %s" %
                                   anyconfig.globals.VERSION)
    parser.set_defaults(**defaults)

    lpog = optparse.OptionGroup(parser, "List specific options")
    lpog.add_option("-L", "--list", help="List supported config types",
                    action="store_true")
    parser.add_option_group(lpog)

    spog = optparse.OptionGroup(parser, "Schema specific options")
    spog.add_option("", "--validate", action="store_true",
                    help="Only validate input files and do not output. "
                         "You must specify schema file with -S/--schema "
                         "option.")
    spog.add_option("", "--gen-schema", action="store_true",
                    help="Generate JSON schema for givne config file[s] "
                         "and output it instead of (merged) configuration.")
    parser.add_option_group(spog)

    gspog = optparse.OptionGroup(parser, "Get/set options")
    gspog.add_option("", "--get", help=_GET_HELP)
    gspog.add_option("", "--set", help=_SET_HELP)
    parser.add_option_group(gspog)

    parser.add_option("-o", "--output", help="Output file path")
    parser.add_option("-I", "--itype", choices=ctypes,
                      help=(type_help % "Input"))
    parser.add_option("-O", "--otype", choices=ctypes,
                      help=(type_help % "Output"))
    parser.add_option("-M", "--merge", choices=mts, help=mt_help)
    parser.add_option("-A", "--args", help="Argument configs to override")
    parser.add_option("", "--atype", choices=ctypes,
                      help=_ATYPE_HELP_FMT % ctypes_s)

    parser.add_option("-x", "--ignore-missing", action="store_true",
                      help="Ignore missing input files")
    parser.add_option("-T", "--template", action="store_true",
                      help="Enable template config support")
    parser.add_option("-E", "--env", action="store_true",
                      help="Load configuration defaults from "
                           "environment values")
    parser.add_option("-S", "--schema", help="Specify Schema file[s] path")
    parser.add_option("-s", "--silent", action="store_const", dest="loglevel",
                      const=0, help="Silent or quiet mode")
    parser.add_option("-q", "--quiet", action="store_const", dest="loglevel",
                      const=0, help="Same as --silent option")
    parser.add_option("-v", "--verbose", action="store_const", dest="loglevel",
                      const=2, help="Verbose mode")

    if argv is None:
        argv = sys.argv

    (options, args) = parser.parse_args(argv[1:])
    return (parser, options, args)


def _exit_with_output(content, exit_code=0):
    """
    Exit the program with printing out messages.

    :param content: content to print out
    :param exit_code: Exit code
    """
    (sys.stdout if exit_code == 0 else sys.stderr).write(content + "\n")
    sys.exit(exit_code)


def _check_options_and_args(parser, options, args):
    """
    Show supported config format types or usage.

    :param parser: Option parser object
    :param options: Options optparse.OptionParser.parse_args returns
    :param args: Arguments optparse.OptionParser.parse_args returns
    """
    if not args:
        if options.list:
            tlist = ", ".join(API.list_types())
            _exit_with_output("Supported config types: " + tlist)
        else:
            parser.print_usage()
            sys.exit(1)

    if options.validate and options.schema is None:
        _exit_with_output("--validate option requires --scheme option", 1)


def _exit_if_load_failure(cnf, msg):
    """
    :param cnf: Loaded configuration object or None indicates load failure
    :param msg: Message to print out if failure
    """
    if cnf is None:
        _exit_with_output(msg, 1)


def _exit_if_only_to_validate(only_to_validate):
    """
    :param only_to_validate: True if it's only to validate
    """
    if only_to_validate:
        _exit_with_output("Validation succeds")


def _do_get(cnf, get_path):
    """
    :param cnf: Configuration object to print out
    :param get_path: key path given in --get option
    :return: updated Configuration object if no error
    """
    (cnf, err) = API.get(cnf, get_path)
    if cnf is None:  # Failed to get the result.
        _exit_with_output("Failed to get result: err=%s" % err, 1)

    return cnf


def _output_result(cnf, outpath, otype, inpath, itype):
    """
    :param cnf: Configuration object to print out
    :param outpath: Output file path or None
    :param otype: Output type or None
    :param inpath: Input file path
    :param itype: Input type or None
    """
    if not outpath or outpath == "-":
        outpath = sys.stdout
        if otype is None:
            if itype is None:
                try:
                    otype = API.find_loader(inpath).type()
                except AttributeError:
                    _exit_with_output("Specify inpath and/or outpath type[s] "
                                      "with -I/--itype or -O/--otype option "
                                      "explicitly", 1)
            else:
                otype = itype

    if anyconfig.mdicts.is_dict_like(cnf):
        API.dump(cnf, outpath, otype)
    else:
        _exit_with_output(str(cnf))  # Output primitive types as it is.


def main(argv=None):
    """
    :param argv: Argument list to parse or None (sys.argv will be set).
    """
    (parser, options, args) = parse_args(argv=argv)
    API.LOGGER.setLevel(to_log_level(options.loglevel))

    _check_options_and_args(parser, options, args)

    cnf = API.to_container(os.environ.copy() if options.env else {})
    diff = API.load(args, options.itype,
                    ignore_missing=options.ignore_missing,
                    ac_merge=options.merge, ac_template=options.template,
                    ac_schema=options.schema)

    _exit_if_load_failure(diff, "Failed to load: args=%s" % ", ".join(args))
    cnf.update(diff)

    if options.args:
        diff = anyconfig.parser.parse(options.args)
        cnf.update(diff)

    _exit_if_only_to_validate(options.validate)

    if options.gen_schema:
        cnf = API.gen_schema(cnf)

    if options.get:
        cnf = _do_get(cnf, options.get)

    if options.set:
        (key, val) = options.set.split('=')
        API.set_(cnf, key, anyconfig.parser.parse(val))

    _output_result(cnf, options.output, options.otype, args[0], options.itype)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
