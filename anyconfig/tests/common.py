#
# Copyright (C) 2011 - 2016 Satoru SATOH <ssato at redhat.com>
#
# pylint: disable=missing-docstring
import os.path
import tempfile
import unittest

import anyconfig.compat
import m9dicts

from anyconfig.compat import OrderedDict


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


def dicts_equal(dic, ref, ordered=False):
    """Compare (maybe nested) dicts.
    """
    fnc = list if ordered else len
    if fnc(dic.keys()) != fnc(ref.keys()):
        return False

    for key in ref.keys():
        if key not in dic:
            return False

        (next_dic, next_ref) = (dic[key], ref[key])
        if m9dicts.is_dict_like(next_ref):
            if not m9dicts.is_dict_like(next_dic):
                return False

            if not dicts_equal(next_dic, next_ref):
                return False
        else:
            if next_dic != next_ref:
                return False

    return True


def to_bytes(astr):
    """
    Convert a string to bytes. Do nothing in python 2.6.
    """
    return bytes(astr, 'utf-8') if anyconfig.compat.IS_PYTHON_3 else astr


class Test(unittest.TestCase):

    def test_dicts_equal(self):
        dic0 = {'a': 1}
        dic1 = OrderedDict((('a', [1, 2, 3]),
                            ('b', OrderedDict((('c', "CCC"), )))))
        dic2 = dic1.copy()
        dic2["b"] = None

        dic3 = OrderedDict((('b', OrderedDict((('c', "CCC"), ))),
                            ('a', [1, 2, 3])))

        self.assertTrue(dicts_equal({}, {}))
        self.assertTrue(dicts_equal(dic0, dic0))
        self.assertTrue(dicts_equal(dic1, dic1))
        self.assertTrue(dicts_equal(dic2, dic2))
        self.assertTrue(dicts_equal(dic1, dic3))

        self.assertFalse(dicts_equal(dic0, {}))
        self.assertFalse(dicts_equal(dic0, dic1))
        self.assertFalse(dicts_equal(dic1, dic2))
        self.assertFalse(dicts_equal(dic1, dic3, ordered=True))

# vim:sw=4:ts=4:et:
