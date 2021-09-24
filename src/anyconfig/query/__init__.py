#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Public API to query data with JMESPath expression."""
try:
    from .query import try_query
    SUPPORTED = True
except ImportError:
    from .default import try_query
    SUPPORTED = False  # type: ignore


__all__ = [
    'try_query',
]

# vim:sw=4:ts=4:et:
