#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Misc utility routines for anyconfig module."""
import itertools
import typing


def groupby(
    itr: typing.Iterable[typing.Any],
    key_fn: typing.Optional[typing.Callable[..., typing.Any]] = None
) -> typing.Iterable[
        typing.Tuple[typing.Any, typing.Iterable[typing.Any]]
]:
    """Provide an wrapper function of itertools.groupby to sort each results.

    :param itr: Iterable object, a list/tuple/genrator, etc.
    :param key_fn: Key function to sort 'itr'.
    """
    return itertools.groupby(sorted(itr, key=key_fn), key=key_fn)


def concat(xss: typing.Iterable[typing.Iterable[typing.Any]]
           ) -> typing.List[typing.Any]:
    """Concatenates a list of lists."""
    return list(itertools.chain.from_iterable(xs for xs in xss))

# vim:sw=4:ts=4:et:
