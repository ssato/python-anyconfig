#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Misc utility functions."""
import typing


def noop(val: typing.Any, *_args, **_kwargs) -> typing.Any:
    """Do nothing.

    >>> noop(1)
    1
    """
    return val


def filter_options(keys: typing.Iterable[str],
                   options: typing.Mapping[str, typing.Any]
                   ) -> typing.Dict[str, typing.Any]:
    """Filter 'options' with given 'keys'.

    :param keys: key names of optional keyword arguments
    :param options: optional keyword arguments to filter with 'keys'

    >>> filter_options(("aaa", ), dict(aaa=1, bbb=2))
    {'aaa': 1}
    >>> filter_options(("aaa", ), dict(bbb=2))
    {}
    """
    return dict((k, options[k]) for k in keys if k in options)

# vim:sw=4:ts=4:et:
