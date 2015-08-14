#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato at redhat.com>
#
# pylint: disable=missing-docstring
import os.path
import tempfile

import anyconfig.compat


CNF_0 = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
SCM_0 = {"type": "object",
         "properties": {
             "name": {"type": "string"},
             "a": {"type": "integer"},
             "b": {"type": "object",
                   "properties": {
                       "b": {"type": "array",
                             "items": {"type": "integer"}}}}}}


def selfdir():
    """
    >>> os.path.exists(selfdir())
    True
    """
    return os.path.dirname(__file__)


def setup_workdir():
    """
    >>> workdir = setup_workdir()
    >>> assert workdir != '.'
    >>> assert workdir != '/'
    >>> os.path.exists(workdir)
    True
    >>> os.rmdir(workdir)
    """
    return tempfile.mkdtemp(dir="/tmp", prefix="python-anyconfig-tests-")


def cleanup_workdir(workdir):
    """
    FIXME: Danger!

    >>> workdir = setup_workdir()
    >>> os.path.exists(workdir)
    True
    >>> open(os.path.join(workdir, "workdir.stamp"), 'w').write("OK!\n")
    >>> cleanup_workdir(workdir)
    >>> os.path.exists(workdir)
    False
    """
    assert workdir != '/'
    assert workdir != '.'

    os.system("rm -rf " + workdir)


def dicts_equal(lhs, rhs):
    """
    >>> dicts_equal({}, {})
    True
    >>> dicts_equal({}, {'a': 1})
    False
    >>> d0 = {'a': 1}; dicts_equal(d0, d0)
    True
    >>> d1 = {'a': [1, 2, 3]}; dicts_equal(d1, d1)
    True
    >>> dicts_equal(d0, d1)
    False
    """
    if len(lhs.keys()) != len(rhs.keys()):
        return False

    for key, val in anyconfig.compat.iteritems(rhs):
        val_ref = lhs.get(key, None)
        if val != val_ref:
            return False

    return True


def to_bytes(astr):
    """
    Convert a string to bytes. Do nothing in python 2.6.
    """
    return bytes(astr, 'utf-8') if anyconfig.compat.IS_PYTHON_3 else astr

# vim:sw=4:ts=4:et:
