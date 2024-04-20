#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"""Misc utility routines for anyconfig module."""
from __future__ import annotations

import collections.abc
import itertools
import typing


def groupby(
    itr: collections.abc.Iterable[typing.Any],
    key_fn: typing.Optional[collections.abc.Callable[..., typing.Any]] = None
) -> collections.abc.Iterable[
        tuple[typing.Any, collections.abc.Iterable[typing.Any]]
]:
    """Provide an wrapper function of itertools.groupby to sort each results.

    :param itr: Iterable object, a list/tuple/genrator, etc.
    :param key_fn: Key function to sort 'itr'.
    """
    return itertools.groupby(sorted(itr, key=key_fn), key=key_fn)


def concat(
    xss: collections.abc.Iterable[collections.abc.Iterable[typing.Any]]
) -> list[typing.Any]:
    """Concatenates a list of lists."""
    return list(itertools.chain.from_iterable(xs for xs in xss))
