#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Classes to load data sets.
"""
from . import paths


class TDI:
    """A base class to `inject` datasets for loaders and dumpers to test."""
    _cid: str = ""
    _is_loader: bool = True

    keep_order: bool = False
    _data = None

    @classmethod
    def cid(cls) -> str:
        return cls._cid

    @classmethod
    def is_loader(cls) -> bool:
        return cls._is_loader

    def __init__(self, keep_order: bool = False):
        """Initialize members."""
        self.topdir = paths.get_resource_dir(self.cid(), self.is_loader())
        self.keep_order = keep_order

    def load(self):
        self._data = paths.load_data(self.topdir, keep_order=self.keep_order)

    def get(self):
        if self._data is None:
            self.load()

        return self._data
