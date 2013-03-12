#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
import anyconfig.api as A

import codecs
import locale
import logging
import optparse
import sys


__enc = locale.getdefaultlocale()[1]
sys.stdout = codecs.getwriter(__enc)(sys.stdout)
sys.stderr = codecs.getwriter(__enc)(sys.stderr)


DEFAULTS = dict(debug=False, list=False, output=None, itype=None, otype=None,
                atype=None, merge=A.MS_DICTS)

USAGE = """\
%prog [Options...] CONF_PATH_OR_PATTERN_0 [CONF_PATH_OR_PATTERN_1 ..]

Examples:
  %prog --list
  %prog -I yaml /etc/xyz/conf.d/a.conf
  %prog -I yaml '/etc/xyz/conf.d/*.conf' -o xyz.conf --otype json
  %prog '/etc/xyz/conf.d/*.json' -o xyz.yml \\
    --atype json -A '{"obsoletes": "sysdata", "conflicts": "sysdata-old"}'
  %prog '/etc/xyz/conf.d/*.json' -o xyz.yml \\
    -A obsoletes:sysdata;conflicts:sysdata-old
  %prog /etc/foo.json /etc/foo/conf.d/x.json /etc/foo/conf.d/y.json
  %prog '/etc/foo.d/*.json' -M noreplace
"""


def option_parser(defaults=DEFAULTS, usage=USAGE):
    ctypes = A.list_types()
    ctypes_s = ", ".join(ctypes)
    type_help = "Select type of %s config files from " + \
        ctypes_s + " [Automatically detected by file ext]"

    mts = A.MERGE_STRATEGIES.keys()
    mts_s = ", ".join(mts)
    mt_help = "Select strategy to merge multiple configs from " + \
        mts_s + " [%(merge)s]" % defaults

    af_help = """Explicitly select type of argument to provide configs from %s.

If this option is not set, original parser is used: 'K:V' will become {K: V},
'K:V_0,V_1,..' will become {K: [V_0, V_1, ...]}, and 'K_0:V_0;K_1:V_1' will
become {K_0: V_0, K_1: V_1} (where the tyep of K is str, type of V is one of
Int, str, etc.""" % ctypes_s

    p = optparse.OptionParser(usage)
    p.set_defaults(**defaults)

    p.add_option("-D", "--debug", action="store_true", help="Debug mode")
    p.add_option("-L", "--list", help="List supported config types",
                 action="store_true")
    p.add_option("-o", "--output", help="Output file path")
    p.add_option("-I", "--itype", choices=ctypes, help=(type_help % "Input"))
    p.add_option("-O", "--otype", choices=ctypes, help=(type_help % "Output"))
    p.add_option("-M", "--merge", choices=mts, help=mt_help)

    p.add_option("-A", "--args", help="Argument configs to override")
    p.add_option("", "--atype", choices=ctypes, help=af_help)

    return p


def main(argv=sys.argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    llvl = logging.DEBUG if options.debug else logging.INFO
    logging.basicConfig(level=llvl)

    if not args:
        if options.list:
            sys.stdout.write(
                "Supported config types: " + ", ".join(A.list_types()) + "\n"
            )
            sys.exit(0)
        else:
            p.print_usage()
            sys.exit(-1)

    data = A.load(args, options.itype, options.merge)

    if options.args:
        diff = A.loads(options.args, options.atype)
        data.update(diff, options.merge)

    if options.output:
        cp = A.find_loader(options.output, options.otype)
        cp.dump(data, options.output)
    else:
        assert options.otype is not None, \
            "Please specify Output type w/ -O/--otype option"

        cp = A.find_loader(None, options.otype)
        sys.stdout.write(cp.dumps(data))


if __name__ == '__main__':
    main(sys.argv)


# vim:sw=4:ts=4:et:
