#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
# pylint: disable=W0611,F0401,C0111
import sys
import itertools


IS_PYTHON_3 = sys.version_info[0] == 3


# Borrowed from library doc, 9.7.1 Itertools functions:
def _from_iterable(iterables):
    """
    itertools.chain.from_iterable alternative.

    >>> list(_from_iterable([[1, 2], [3, 4]]))
    [1, 2, 3, 4]
    """
    for it in iterables:
        for element in it:
            yield element


def py3_iteritems(dic):
    """wrapper for dict.items() in python 3.x.

    >>> list(py3_iteritems({}))
    []
    >>> sorted(py3_iteritems(dict(a=1, b=2)))
    [('a', 1), ('b', 2)]
    """
    return dic.items()


def py3_cmp(a, b):
    """
    >>> py3_cmp(0, 2)
    -1
    >>> py3_cmp(4, 4)
    0
    >>> py3_cmp(3, 1)
    1
    """
    return (a > b) - (a < b)


if IS_PYTHON_3:
    import configparser  # flake8: noqa
    from io import StringIO  # flake8: noqa
    iteritems = py3_iteritems
    from_iterable = itertools.chain.from_iterable
    cmp = py3_cmp
else:
    import ConfigParser as configparser  # flake8: noqa
    try:
        from cStringIO import StringIO  # flake8: noqa
    except ImportError:
        from StringIO import StringIO  # flake8: noqa

    try:
        from_iterable = itertools.chain.from_iterable
    except AttributeError:
        from_iterable = _from_iterable

    assert configparser  # silence pyflakes
    assert StringIO  # ditto

    def py_iteritems(dic):
        """wrapper for dict.iteritems() in python < 3.x

        >>> list(py_iteritems({}))
        []
        >>> sorted(py_iteritems(dict(a=1, b=2)))
        [('a', 1), ('b', 2)]
        """
        return dic.iteritems()

    iteritems = py_iteritems
    cmp = cmp

# vim:sw=4:ts=4:et:
