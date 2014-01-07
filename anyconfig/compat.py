#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
# pylint: disable=W0611,F0401,C0111
import sys


IS_PYTHON_3 = sys.version_info[0] == 3

if IS_PYTHON_3:
    import configparser
    from io import StringIO

    def iteritems(dic):
        """wrapper for dict.items()"""
        return dic.items()
else:
    import ConfigParser as configparser
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

    def iteritems(dic):
        """wrapper for dict.iteritems()"""
        return dic.iteritems()

# vim:sw=4:ts=4:et:
