#
# Copyright (C) 2023, 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,too-few-public-methods
r"""Classes to load data sets.
"""
import pathlib
import re
import typing

import anyconfig.ioinfo

from . import paths


def name_from_path(path: str):
    """Compute a name from given path `path`."""
    match = re.match(r".+/test_([^_]+)_([^_]+).py", path)
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

    _data = None

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

    def get(self):
        if self._data is None:
            self.load()

        return self._data

    def gets(self):
        data = self.get()
        data_ids = [f"{i.parent.name}/{i.name}" for i, _aux in data]

        return (data, data_ids)


class Base:
    """Base class for backend test cases.
    """
    psr_cls = None

    def assert_loads_and_load_impl(
        self, ipath: pathlib.Path, aux: typing.Dict[str, typing.Any],
        debug: bool = False,
    ):
        exp = aux["e"]  # It should NOT fail.
        opt = aux.get("o", {})
        ioi = anyconfig.ioinfo.make(ipath)

        if self.psr_cls is None:
            return

        psr = self.psr_cls()

        if debug:
            assert not exp, exp
            assert not opt, opt

        assert psr.loads(ipath.read_text(), **opt) == exp
        assert psr.load(ioi, **opt) == exp
