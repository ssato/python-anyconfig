#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.single_load with template args."""
from __future__ import annotations

import warnings

import pytest

import anyconfig.api._load as TT
try:
    import anyconfig.template.jinja2  # pylint: disable=unused-import
except ImportError:
    pytest.skip(
        "Requried jinja2 lib is not available.",
        allow_module_level=True
    )

from . import common


DATASETS = common.load_datasets("template")


@pytest.mark.parametrize(("ipath", "ctx", "exp", "opts"), DATASETS)
def test_single_load(ipath, ctx, exp, opts):
    assert TT.single_load(ipath, ac_context=ctx, **opts) == exp


def test_single_load_from_invalid_template(tmp_path):
    ipath = tmp_path / 'test.json'
    ipath.write_text('{"a": "{{ a"}')  # broken template string.

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter('always')
        res = TT.single_load(ipath, ac_template=True, ac_context={"a": 1})

        assert res == {"a": '{{ a'}
        assert len(warns) > 0
        assert issubclass(warns[-1].category, UserWarning)
        assert 'ailed to compile ' in str(warns[-1].message)
