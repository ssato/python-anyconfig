#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
r"""Classes to load data sets.
"""
import importlib
import os
import re

from . import paths


def name_from_path(path: str):
    """Compute a name from given path `path`."""
    match = re.match(
        r".+"
        f"{os.path.sep}"
        r"test_([^_]+)_([^_]+).py",
        path
    )
    if not match:
        raise NameError(f"Filename does not match expected pattern: {path}")

    return ".".join(match.groups())


class TDI:
    """A base class to `inject` datasets for loaders and dumpers to test."""
    _path: str = ""

    # Override it in children:
    # _cid: str = name_from_path(__file__)
    _cid: str = ""
    _is_loader: bool = True

    _data = []
    _mod = None

    @classmethod
    def cid(cls) -> str:
        return cls._cid

    @classmethod
    def is_loader(cls) -> bool:
        return cls._is_loader

    def __init__(self):
        """Initialize members."""
        self.topdir = paths.get_resource_dir(self.cid(), self.is_loader())

    def load(self):
        self._data = paths.load_data(self.topdir)

    def get_data(self):
        if not self._data:
            try:
                self.load()
            except FileNotFoundError:
                pass

        return self._data

    def get_data_ids(self):
        return [f"{i.parent.name}/{i.name}" for i, _aux in self.get_data()]

    def get_mod(self):
        if self._mod is None:
            mname = f"anyconfig.backend.{self.cid()}"
            try:
                self._mod = importlib.import_module(mname)
            except ModuleNotFoundError:
                pass

        return self._mod

    def get_all(self):
        return (self.get_mod(), self.get_data(), self.get_data_ids())
