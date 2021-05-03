#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""misc global constants, variables, classes and so on.
"""
try:
    from .jsonschema_ import validate, gen_schema
    SUPPORTED: bool = True
except ImportError:
    from .default import validate, gen_schema
    SUPPORTED = False  # type: ignore


__all__ = [
    'validate', 'gen_schema', 'SUPPORTED'
]

# vim:sw=4:ts=4:et:
