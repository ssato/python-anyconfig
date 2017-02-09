#
# Copyright (C) 2011 - 2015 Red Hat, Inc.
# Copyright (C) 2011 - 2017 Satoru SATOH <ssato redhat.com>
# License: MIT
#
# pylint: disable=import-error,unused-import
"""Module to keep backward compatibilities.

- basic str types are different in python 2.x and 3.x.
- collections.ordereddict is not available in python 2.6.
"""
from __future__ import absolute_import

import sys

try:
    from collections import OrderedDict  # flake8: noqa
except ImportError:
    from ordereddict import OrderedDict  # flake8: noqa

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

try:
    STR_TYPES = (basestring, unicode)  # flake8: noqa
except NameError:
    STR_TYPES = (str, )  # flake8: noqa


def to_str(obj):
    """
    :return: String representation of given object
    """
    return str(obj).encode("utf-8") if sys.version_info[0] == 3 else str(obj)

# vim:sw=4:ts=4:et:
