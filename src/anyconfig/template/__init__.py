#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""misc global constants, variables, classes and so on.
"""
try:
    from .jinja2_ import try_render
    SUPPORTED: bool = True
except ImportError:  # jinja2 may not be available.
    SUPPORTED = False  # type: ignore

    def try_render(*_args, **_kwargs) -> None:
        """Dummy function does nothing but returns None.
        """
        return None


__all__ = [
    'try_render',
]

# vim:sw=4:ts=4:et:
