#
# Copyright (C) 2011 - 2016 Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""Wrapper of m9dicts.

.. versionadded: 0.4.99
   Swtiched from mergeabledict to m9dicts
"""
from __future__ import absolute_import

import m9dicts
from m9dicts import (
    MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS, MERGE_STRATEGIES,
    get, set_  # flake8: noqa
)


NTPL_CLS_KEY = "ntpl_cls_key__"


def to_container(obj=None, ac_ordered=False, ac_merge=m9dicts.MS_DICTS,
                 ac_ntpl_cls_key=NTPL_CLS_KEY, **options):
    """
    Factory function to create a dict-like object[s] supports merge operation
    from a dict or any other objects.

    .. seealso:: :func:`m9dicts.make`

    :param obj: A dict or other object[s] or None
    :param ordered:
        Create an instance of OrderedMergeableDict instead of MergeableDict If
        it's True. Please note that OrderedMergeableDict class will be chosen
        for namedtuple objects regardless of this argument always to keep keys
        (fields) order.
    :param merge:
        Specify strategy from MERGE_STRATEGIES of how to merge results loaded
        from multiple configuration files.
    :param _ntpl_cls_key:
        Special keyword to embedded the class name of namedtuple object to the
        MergeableDict object created. It's a hack and not elegant but I don't
        think there are another ways to make same namedtuple object from the
        MergeableDict object created from it.
    :param options:
        Optional keyword arguments for m9dicts.convert_to, will be converted to
        the above ac_\* options respectively as needed.
    """
    opts = dict(ordered=options.get("ordered", ac_ordered),
                merge=options.get("merge", ac_merge),
                _ntpl_cls_key=options.get("_ntpl_cls_key", ac_ntpl_cls_key))

    return m9dicts.make(obj, **opts)


def convert_to(obj, ac_ordered=True, ac_namedtuple=False,
               ac_ntpl_cls_key=NTPL_CLS_KEY, **options):
    """
    Convert given `obj` :: m9dict object to a dict, dict or OrderedDict if
    ac_ordered == True, or a namedtuple if ac_namedtuple == True.

    .. seealso:: :func:`m9dicts.convert_to`

    :param obj: A m9dict object to convert to
    :param ac_ordered: OrderedDict will be chosen if True
    :param ac_namedtuple: A namedtuple object will be chosen if True
    :param ac_ntpl_cls_key: The name of namedtuple object
    :param options:
        Optional keyword arguments for m9dicts.convert_to, will be converted to
        the above ac_\* options respectively as needed.
    """
    opts = dict(ordered=options.get("ordered", ac_ordered),
                to_namedtuple=options.get("to_namedtuple", ac_namedtuple),
                _ntpl_cls_key=options.get("_ntpl_cls_key", ac_ntpl_cls_key))

    return m9dicts.convert_to(obj, **opts)

# vim:sw=4:ts=4:et:
