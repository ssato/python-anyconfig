#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
"""Provides utility functions in anyconfig.backend.base."""
import functools
import pathlib
import typing


def not_implemented(*_args, **_kwargs) -> None:
    """Raise NotImplementedError."""
    raise NotImplementedError()


def ensure_outdir_exists(filepath: typing.Union[str, pathlib.Path]) -> None:
    """Make dir to dump 'filepath' if that dir does not exist.

    :param filepath: path of file to dump
    """
    pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)


def to_method(func: typing.Callable[..., typing.Any]
              ) -> typing.Callable[..., typing.Any]:
    """Lift :func:`func` to a method.

    It will be called with the first argument 'self' ignored.

    :param func: Any callable object
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Original function decorated."""
        return func(*args[1:], **kwargs)

    return wrapper

# vim:sw=4:ts=4:et:
