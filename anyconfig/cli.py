#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
import anyconfig.api as A
import anyconfig.compat
import anyconfig.globals

import codecs
import locale
import logging
import optparse
import sys


_ENCODING = locale.getdefaultlocale()[1]
A.LOGGER.addHandler(logging.StreamHandler())

if anyconfig.compat.IS_PYTHON_3:
    import io

    _ENCODING = _ENCODING.lower()

    # FIXME: Fix the error, "AttributeError: '_io.StringIO' object has no
    # attribute 'buffer'".
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
  %prog --list
  %prog -I yaml -O yaml /etc/xyz/conf.d/a.conf
  %prog -I yaml '/etc/xyz/conf.d/*.conf' -o xyz.conf --otype json
  %prog '/etc/xyz/conf.d/*.json' -o xyz.yml \\
    --atype json -A '{"obsoletes": "sysdata", "conflicts": "sysdata-old"}'
  %prog '/etc/xyz/conf.d/*.json' -o xyz.yml \\
    -A obsoletes:sysdata;conflicts:sysdata-old
  %prog /etc/foo.json /etc/foo/conf.d/x.json /etc/foo/conf.d/y.json
  %prog '/etc/foo.d/*.json' -M noreplace
  %prog '/etc/foo.d/*.json' --get a.b.c
  %prog '/etc/foo.d/*.json' --set a.b.c=1"""


def to_log_level(level):
    """
    :param level: Logging level in int = 0 .. 2
    """
    assert level >= 0 and level < 3, "wrong log level passed: " + str(level)
    return [logging.WARN, logging.INFO, logging.DEBUG][level]


def option_parser(defaults=None, usage=USAGE):
    """
    Make up an option and arguments parser.

    :param defaults: Default option values
    :param usage: Usage text
    """
    defaults = dict(loglevel=1, list=False, output=None, itype=None,
                    otype=None, atype=None, merge=A.MS_DICTS,
                    ignore_missing=False, template=True)

    ctypes = A.list_types()
    ctypes_s = ", ".join(ctypes)
    type_help = "Select type of %s config files from " + \
        ctypes_s + " [Automatically detected by file ext]"

    mts = A.MERGE_STRATEGIES
    mts_s = ", ".join(mts)
    mt_help = "Select strategy to merge multiple configs from " + \
        mts_s + " [%(merge)s]" % defaults

    af_help = """Explicitly select type of argument to provide configs from %s.

If this option is not set, original parser is used: 'K:V' will become {K: V},
'K:V_0,V_1,..' will become {K: [V_0, V_1, ...]}, and 'K_0:V_0;K_1:V_1' will
become {K_0: V_0, K_1: V_1} (where the tyep of K is str, type of V is one of
Int, str, etc.""" % ctypes_s

    get_help = ("Specify key path to get part of config, for example, "
                "'--get a.b.c' to config {'a': {'b': {'c': 0, 'd': 1}}} "
                "gives 0 and '--get a.b' to the same config gives "
                "{'c': 0, 'd': 1}.")
    set_help = ("Specify key path to set (update) part of config, for "
                "example, '--set a.b.c=1' to a config {'a': {'b': {'c': 0, "
                "'d': 1}}} gives {'a': {'b': {'c': 1, 'd': 1}}}.")

    parser = optparse.OptionParser(usage, version="%%prog %s" %
                                   anyconfig.globals.VERSION)
    parser.set_defaults(**defaults)

    parser.add_option("-L", "--list", help="List supported config types",
                      action="store_true")
    parser.add_option("-o", "--output", help="Output file path")
    parser.add_option("-I", "--itype", choices=ctypes,
                      help=(type_help % "Input"))
    parser.add_option("-O", "--otype", choices=ctypes,
                      help=(type_help % "Output"))
    parser.add_option("-M", "--merge", choices=mts, help=mt_help)
    parser.add_option("-A", "--args", help="Argument configs to override")
    parser.add_option("", "--atype", choices=ctypes, help=af_help)

    parser.add_option("", "--get", help=get_help)
    parser.add_option("", "--set", help=set_help)

    parser.add_option("-x", "--ignore-missing", action="store_true",
                      help="Ignore missing input files")
    parser.add_option("", "--no-template", dest="template",
                      action="store_false",
                      help="Disable template config support")

    parser.add_option("-s", "--silent", action="store_const", dest="loglevel",
                      const=0, help="Silent or quiet mode")
    parser.add_option("-q", "--quiet", action="store_const", dest="loglevel",
                      const=0, help="Same as --silent option")
    parser.add_option("-v", "--verbose", action="store_const", dest="loglevel",
                      const=2, help="Verbose mode")

    return parser


# pylint: disable=W0102
def main(argv=sys.argv):
    """
    :param argv: Argument list to parse [sys.argv]
    """
    parser = option_parser()
    (options, args) = parser.parse_args(argv[1:])

    A.set_loglevel(to_log_level(options.loglevel))

    if not args:
        if options.list:
            tlist = ", ".join(A.list_types()) + "\n"
            sys.stdout.write("Supported config types: " + tlist)
            sys.exit(0)
        else:
            parser.print_usage()
            sys.exit(-1)

    data = A.load(args, options.itype, options.merge,
                  ignore_missing=options.ignore_missing,
                  template=options.template)

    if options.args:
        diff = A.loads(options.args, options.atype)
        data.update(diff, options.merge)

    if options.get:
        (data, err) = A.get(data, options.get)
        if err:
            raise RuntimeError(err)

    if options.set:
        A.set_(data, *(options.set.split('=')))

    if options.output:
        cparser = A.find_loader(options.output, options.otype)
        if cparser is None:
            raise RuntimeError("No suitable dumper was found for %s",
                               options.output)

        cparser.dump(data, options.output)
    else:
        # TODO: Reuse input type automatically detected as it's impossible to
        # detect output type w/o options.output.
        if options.otype is None:
            if options.itype is None:
                raise RuntimeError("Please specify input and/or output type "
                                   "with -I (--itype) or -O (--otype) option")
            else:
                options.otype = options.itype

        cparser = A.find_loader(None, options.otype)
        sys.stdout.write(cparser.dumps(data))


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
