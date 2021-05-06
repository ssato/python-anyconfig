#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
r"""Utility functions in anyconfig.backend.base.
"""
import functools
import pathlib


def ensure_outdir_exists(filepath):
    """
    Make dir to dump 'filepath' if that dir does not exist.

    :param filepath: path of file to dump
    """
    pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)


def to_method(func):
    """
    Lift :func:`func` to a method; it will be called with the first argument
    'self' ignored.

    :param func: Any callable object
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function.
        """
        return func(*args[1:], **kwargs)

    return wrapper

# vim:sw=4:ts=4:et:
