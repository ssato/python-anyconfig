#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Ref. python -c "import toml; help(toml); ..."
#
# pylint: disable=unused-argument
"""TOML backend.

- TOML: https://github.com/toml-lang/toml
- (python) toml module: https://github.com/uiri/toml
"""
from __future__ import absolute_import

import functools
import toml
import anyconfig.backend.json


def call_with_no_kwargs(func):
    """
    Call :func:`func` without given keyword args

    :param func: Any callable object

    >>> call_with_no_kwargs(len)([], kwarg0_ignored=True)
    0
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function.
        """
        return func(*args)

    return wrapper


class Parser(anyconfig.backend.json.Parser):
    """
    Loader/Dumper for TOML configs:

    - Backend: toml (https://github.com/uiri/toml)
    - Limitations: None obvious
    - Special options: None (_dict is not supported)
    """
    _type = "toml"
    _extensions = ["toml"]
    _funcs = dict(loads=call_with_no_kwargs(toml.loads),
                  load=call_with_no_kwargs(toml.load),
                  dumps=call_with_no_kwargs(toml.dumps),
                  dump=call_with_no_kwargs(toml.dump))

# vim:sw=4:ts=4:et:
