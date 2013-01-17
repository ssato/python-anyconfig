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


USAGE = """\
%prog [Options...] CONF_PATH_OR_PATTERN_0 [CONF_PATH_OR_PATTERN_1 ..]

Examples:
  %prog --list
  %prog -I yaml /etc/xyz/conf.d/a.conf
  %prog -I yaml '/etc/xyz/conf.d/*.conf' -o xyz.conf --otype json
  %prog /etc/foo.json /etc/foo/conf.d/x.json /etc/foo/conf.d/y.json
"""


def main(argv=sys.argv):
    defaults = {
        "debug": False,
        "list": False,
        "output": None,
        "itype": None,
        "otype": None,
    }
    ctypes = A.list_types()
    type_help = "Explicitly select type of %s config files from " + \
        ", ".join(ctypes) + " [Automatically detected by file path]"

    p = optparse.OptionParser(USAGE)
    p.set_defaults(**defaults)

    p.add_option("-D", "--debug", action="store_true", help="Debug mode")
    p.add_option("-L", "--list", help="List supported config types",
                 action="store_true")
    p.add_option("-o", "--output", help="Output file path")
    p.add_option("-I", "--itype", choices=ctypes, help=(type_help % "Input"))
    p.add_option("-O", "--otype", choices=ctypes, help=(type_help % "Output"))

    (options, args) = p.parse_args(argv[1:])

    llvl = logging.DEBUG if options.debug else logging.INFO
    logging.basicConfig(level=llvl)

    if not args:
        if options.list:
            sys.stdout.write("Supported config types: " + \
                             ", ".join(A.list_types()) + "\n")
            sys.exit(0)
        else:
            p.print_usage()
            sys.exit(-1)

    data = A.load(args, options.itype)

    if options.output:
        cp = A.find_parser(options.output, options.otype)
        cp.dump(data, options.output)
    else:
        assert options.otype is not None, \
            "Please specify Output type w/ -O/--otype option"
        cp = A.find_parser(None, options.otype)
        sys.stdout.write(cp.dumps(data))


if __name__ == '__main__':
    main(sys.argv)


# vim:sw=4:ts=4:et:
