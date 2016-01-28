#
# Copyright (C) 2011 - 2015 Red Hat, Inc.
# Copyright (C) 2011 - 2016 Satoru SATOH <ssato redhat.com>
# License: MIT
#
# pylint: disable=import-error,unused-import
"""Module to keep backward compatibilities.

- basic str types are different in python 2.x and 3.x.
- collections.ordereddict is not available in python 2.6.
"""
from __future__ import absolute_import

try:
    from collections import OrderedDict  # flake8: noqa
except ImportError:
    from ordereddict import OrderedDict  # flake8: noqa

try:
    STR_TYPES = (basestring, unicode)  # flake8: noqa
except NameError:
    STR_TYPES = (str, )  # flake8: noqa

# vim:sw=4:ts=4:et:
