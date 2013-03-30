#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
import sys


IS_PYTHON_3 = sys.version_info[0] == 3

if IS_PYTHON_3:
    import configparser
    from io import StringIO

    def iteritems(d):
        return d.items()
else:
    import ConfigParser as configparser
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

    def iteritems(d):
        return d.iteritems()

# vim:sw=4:ts=4:et:
