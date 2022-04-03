#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Misc global constants, variables, classes and so on."""
try:
    from .jsonschema import validate, is_valid, gen_schema
    SUPPORTED: bool = True
except ImportError:
    from .default import validate, is_valid, gen_schema
    SUPPORTED = False  # type: ignore


__all__ = [
    'validate', 'is_valid', 'gen_schema', 'SUPPORTED'
]

# vim:sw=4:ts=4:et:
