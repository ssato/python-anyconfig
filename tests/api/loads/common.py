#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import functools
import pathlib
import typing
import unittest

import anyconfig.api

from tests.base import TESTS_DIR


def identity(obj, *_args, **_opts):
    return obj


class TestData(typing.NamedTuple):
    """Equivalent to collections.namedtuple."""
    datadir: pathlib.Path
    path: pathlib.Path
    inp: str
    exp: typing.Union[pathlib.Path, typing.Dict[str, typing.Any]]
    opts: typing.Union[pathlib.Path, typing.Dict[str, typing.Any]]
    scm: pathlib.Path
    query: pathlib.Path
    ctx: pathlib.Path


class BaseTestCase(unittest.TestCase):

    target = 'loads'
    kind = 'basics'
    root = None
    pattern = '*.json'

    @property
    @functools.lru_cache(None)
    def test_data(self):
        # e.g. res/loads/basics/
        self.root = TESTS_DIR / 'res' / self.target / self.kind
        datasets = [
            (datadir,
             [(inp,
               inp.read_text(),  # input data
               datadir / 'e' / inp.name,  # expected data
               datadir / 'o' / inp.name,  # options data
               datadir / 's' / inp.name,  # schema data
               datadir / 'q' / inp.name.replace('.json', '.txt'),  # query data
               datadir / 'c' / inp.name,  # context data
               )
              for inp in sorted(datadir.glob(self.pattern)) if inp.is_file()
              ]
             )
            for datadir in sorted(self.root.glob('*')) if datadir.is_dir()
        ]
        if not datasets:
            raise RuntimeError(f'No data: {self.root!s}')

        for datadir, data in datasets:
            if not data:
                raise RuntimeError(f'No data in subdir: {datadir!s}')

        return datasets

    def each_data(self, load=True):
        load_fn = anyconfig.api.single_load if load else identity
        for datadir, data in self.test_data:
            for path, inp, e_path, o_path, s_path, q_path, c_path in data:
                yield TestData(
                    datadir, path, inp,
                    load_fn(e_path), load_fn(o_path),
                    s_path, q_path, c_path
                )

# vim:sw=4:ts=4:et:
