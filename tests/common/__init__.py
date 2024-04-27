#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
"tests.common - common global variables and functions."""
from .globals_ import RESOURCE_DIR
from .tdc import collect_for

__all__ = [
    "RESOURCE_DIR",
    "collect_for",
]
