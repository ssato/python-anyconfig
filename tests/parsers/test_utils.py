#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.parsers.utils.
"""
from __future__ import annotations

import operator

import pytest

import anyconfig.parsers.parsers
import anyconfig.parsers.utils as TT

from anyconfig.common import (
    UnknownFileTypeError, UnknownProcessorTypeError
)
from anyconfig.backend.json import PARSERS as JSON_PSR_CLSS


PSRS = anyconfig.parsers.parsers.Parsers().list()
JSON_PSRS = sorted(
    (p() for p in JSON_PSR_CLSS),
    key=operator.methodcaller("priority"), reverse=True
)


def test_load_plugins():
    TT.load_plugins()
    assert PSRS


def test_list_types():
    res = TT.list_types()
    assert bool(res)
    assert any(x in res for x in ("json", "ini", "xml"))


def test_list_by_x():
    for lfn in (TT.list_by_cid, TT.list_by_type, TT.list_by_extension):
        psrs = lfn()
        assert bool(psrs)


@pytest.mark.parametrize(
    ("args", "exc"),
    (((None, None), ValueError),  # w/o path nor type
     (("/tmp/x.xyz", None), UnknownFileTypeError),
     (("/dev/null", None), UnknownFileTypeError),
     ((None, "xyz"), UnknownProcessorTypeError),
     )
)
def test_findall_ng_cases(args, exc):
    with pytest.raises(exc):
        TT.findall(*args)


@pytest.mark.parametrize(
    ("obj", "typ"),
    (("foo.json", None),
     (None, "json"),
     )
)
def test_findall(obj, typ):
    psrs = TT.findall(obj=obj, forced_type=typ)

    assert bool(psrs)
    assert psrs == JSON_PSRS


@pytest.mark.parametrize(
    ("obj", "typ"),
    (("foo.json", None),
     (None, "json"),
     (None, JSON_PSR_CLSS[0]),
     (None, JSON_PSRS[0]),
     )
)
def test_find(obj, typ):
    psr = TT.find(obj=obj, forced_type=typ)
    assert psr == JSON_PSRS[0]
