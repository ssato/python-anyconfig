#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Common library for YAML backend modules."""
from ...utils import filter_options
from .. import base


def filter_from_options(key, options):
    """Filter a key ``key`` in ``options.

    :param key: Key str in options
    :param options: Mapping object
    :return:
        New mapping object from 'options' in which the item with 'key' filtered

    >>> filter_from_options('a', dict(a=1, b=2))
    {'b': 2}
    """
    return filter_options([k for k in options.keys() if k != key], options)


class Parser(base.StreamParser):
    """Parser for YAML files."""

    _type = 'yaml'
    _extensions = ['yaml', 'yml']
    _ordered = True
    _allow_primitives = True
    _dict_opts = ['ac_dict']

# vim:sw=4:ts=4:et:
