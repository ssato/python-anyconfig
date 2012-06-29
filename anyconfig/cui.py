#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
import anyconfig.AnyConfig as A
import anyconfig.parser as P

import logging
import optparse
import sys


def main(argv=sys.argv):
    defaults = {
        "debug": False,
        "output": None,
        "type": "json",
    }

    p = optparse.OptionParser(
        "%prog [Options...] INPUT_CONF_0[,INPUT_CONF_1,...]"
    )
    p.set_defaults(**defaults)

    p.add_option("-D", "--debug", action="store_true", help="Debug mode")
    p.add_option("-o", "--output", help="Output filename")
    p.add_option("-t", "--type", help="Output configuration type [%default]")

    (options, args) = p.parse_args(argv[1:])

    if not args:
        p.print_usage()
        sys.exit(-1)

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not options.output:
        options.output = sys.stdout

    cs = P.parse_list_str(args)
    data = A.loads(cs)
    A.dump(data, options.output)


if __name__ == '__main__':
    main(sys.argv)


# vim:sw=4:ts=4:et:
