#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
# pylint: disable=W0611,F0401,C0111
import sys


IS_PYTHON_3 = sys.version_info[0] == 3

if IS_PYTHON_3:
    import configparser  # flake8: noqa
    from io import StringIO  # flake8: noqa

    def iteritems(dic):
        """wrapper for dict.items()"""
        return dic.items()
else:
    import ConfigParser as configparser  # flake8: noqa
    try:
        from cStringIO import StringIO  # flake8: noqa
    except ImportError:
        from StringIO import StringIO  # flake8: noqa

    assert configparser  # silence pyflakes
    assert StringIO  # ditto

    def iteritems(dic):
        """wrapper for dict.iteritems()"""
        return dic.iteritems()

# vim:sw=4:ts=4:et:
