#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=unused-argument
"""Provide dummy implementation of anyconfig.query.*."""
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from ..common import InDataExT
    from .datatypes import MaybeJexp


def try_query(
    data: InDataExT, jexp: MaybeJexp = None, **options
) -> InDataExT:
    """Provide a dummy implementation of :func:`anyconfig.query.try_query`."""
    return data
