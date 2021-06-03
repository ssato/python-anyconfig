#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anyconfig.api

from tests.base import TESTS_DIR, DATA_00


def list_test_data(kind: str = 'basics'):
    root = TESTS_DIR / 'res' / 'loads' / kind
    _ies = sorted(
        (ddir,
         [(inp,
           DATA_00.get(str(inp.resolve()), None)
           )
          for inp in sorted(ddir.glob('*.json')) if inp.is_file()
          ]
         )
        for ddir in root.glob('*') if ddir.is_dir()
    )
    if not _ies:
        raise RuntimeError(f'No data: {root!s}')

    return _ies


class BaseTestCase(unittest.TestCase):

    # see: tests/res/json/basic/
    kind = 'basic'
    root = None

    @property
    def list_inp_exp(self):
        self.root = TESTS_DIR / 'res' / 'json' / self.kind

        _ies = [
            (inp,
             anyconfig.api.single_load(self.root / 'e' / inp.name)
             )
            for inp in sorted(self.root.glob('*.json')) if inp.is_file()
        ]
        if not _ies:
            raise RuntimeError(f'No data: {self.root!s}')

        return _ies

# vim:sw=4:ts=4:et:
