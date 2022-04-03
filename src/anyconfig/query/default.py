#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=unused-argument
"""Provide dummy implementation of anyconfig.query.*."""
from ..common import InDataExT
from .datatypes import MaybeJexp


def try_query(data: InDataExT, jexp: MaybeJexp = None, **options) -> InDataExT:
    """Provide a dummy implementation of :func:`anyconfig.query.try_query`."""
    return data

# vim:sw=4:ts=4:et:
