#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
from tests.base import TESTS_DIR, DATA_00


def list_test_data(kind: str = 'basics'):
    root = TESTS_DIR / 'res' / 'loads' / kind
    _ies = sorted(
        (ddir, sorted(
            (inp, DATA_00.get(str(inp.resolve()), None))
            for inp in ddir.glob('*.json') if inp.is_file()
        ))
        for ddir in root.glob('*') if ddir.is_dir()
    )
    if not _ies or any(not data for ddir, data in _ies):
        raise RuntimeError(f'No data: {root!s}')

    return _ies

# vim:sw=4:ts=4:et:
