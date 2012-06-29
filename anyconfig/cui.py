#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
import anyconfig.AnyConfig as A
import anyconfig.backend.backends as Backends

import codecs
import locale
import logging
import optparse
import sys


__enc = locale.getdefaultlocale()[1]
sys.stdout = codecs.getwriter(__enc)(sys.stdout)
sys.stderr = codecs.getwriter(__enc)(sys.stderr)


def main(argv=sys.argv):
    defaults = {
        "debug": False,
        "output": None,
        "type": "json",
    }

    p = optparse.OptionParser(
        "%prog [Options...] INPUT_CONF_0 [INPUT_CONF_1 ...]"
    )
    p.set_defaults(**defaults)

    p.add_option("-D", "--debug", action="store_true", help="Debug mode")
    p.add_option("-o", "--output", help="Output file path")
    p.add_option("-t", "--type", help="Output configuration type [%default]")

    (options, args) = p.parse_args(argv[1:])

    if not args:
        p.print_usage()
        sys.exit(-1)

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    data = A.loads(args)

    if options.output:
        cp = Backends.find_by_file(options.output)
        cp.dump(data, options.output)
    else:
        cp = Backends.find_by_type(options.type)
        sys.stdout.write(cp.dumps(data))


if __name__ == '__main__':
    main(sys.argv)


# vim:sw=4:ts=4:et:
