#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=unused-argument
r"""Dummy implementation of anyconfig.query.*.
"""
from ..common import InDataT
from .datatypes import MaybeJexp


def try_query(data: InDataT, jexp: MaybeJexp = None, **options) -> InDataT:
    """
    Dummy implementation of :func:`anyconfig.query.try_query`
    """
    return data

# vim:sw=4:ts=4:et:
