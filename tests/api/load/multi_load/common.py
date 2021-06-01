#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
r"""Common utility functions.
"""
import pathlib

import anyconfig.dicts
import anyconfig.api as TT


RES_DIR = pathlib.Path(__file__).parent / '../../../' / 'res'
DIC_0 = anyconfig.dicts.convert_to(dict())


def datasets_itr(kind):
    for rdir in sorted(pathlib.Path(RES_DIR / 'multi' / kind).glob('*')):
        if not rdir.is_dir():
            continue

        exp = TT.single_load(rdir / 'e' / 'exp.json')
        opts = TT.single_load(rdir / 'options' / '00.json')

        yield (rdir, exp, opts)


def gen_datasets(kind='basics'):
    datasets = sorted(datasets_itr(kind))
    if not datasets:
        raise RuntimeError('No test data was found!')

    return datasets

# vim:sw=4:ts=4:et:
