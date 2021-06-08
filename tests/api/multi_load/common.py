#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Common utility functions.
"""
import functools
import unittest

import anyconfig.api as TT

from tests.base import RES_DIR


def datasets_itr(kind):
    for rdir in sorted((RES_DIR / 'multi' / kind).glob('*')):
        if not rdir.is_dir():
            continue

        exp = TT.single_load(rdir / 'e' / 'exp.json')
        opts = TT.single_load(rdir / 'options' / '00.json')

        yield (rdir, exp, opts)


def gen_datasets(kind):
    datasets = sorted(datasets_itr(kind))
    if not datasets:
        raise RuntimeError('No test data was found!')

    return datasets


class BaseTestCase(unittest.TestCase):

    kind = 'basics'

    @property
    @functools.lru_cache(None)
    def datasets(self):
        return gen_datasets(self.kind)

# vim:sw=4:ts=4:et:
