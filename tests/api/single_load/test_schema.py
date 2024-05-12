#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, unused-import
"""Test cases for anyconfig.api.single_load with schema options."""
from __future__ import annotations

import pathlib
import typing
import warnings

import pytest

import anyconfig.api._load as TT

from anyconfig.api import ValidationError

from ... import common

try:
    import jsonschema  # noqa: F401
except ImportError:
    pytest.skip(
        "Required jsonschema lib is not available.",
        allow_module_level=True
    )


SCM_NG_0 = '''{
    "type": "object",
    "properties": {"key_never_exist": {"type": "string", "required": true}}
}'''


def ipath_to_scm_path(ipath: pathlib.Path) -> typing.Optional[pathlib.Path]:
    basename: str = ipath.name.replace(ipath.suffix, "")
    candidates = list((ipath.parent / "s").glob(f"{basename}.*"))
    if candidates:
        return candidates[0]

    return None


NAMES: tuple[str, ...] = ("ipath", "exp", "opts", "scm")
DATA: list = [
    (i, e, o, ipath_to_scm_path(i)) for i, o, e
    in common.load_data_for_testfile(__file__)
]
DATA_IDS: list[str] = common.get_test_ids(DATA)


def test_data() -> None:
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_single_load(ipath, exp, opts, scm):
    assert scm, f"Not found: {scm!s} [{ipath!s}"
    assert TT.single_load(ipath, ac_schema=scm, **opts) == exp


@pytest.mark.parametrize(
    ("ipath", "opts"),
    [(ipath, opts) for ipath, _, opts, _ in DATA[:1]],
    ids=DATA_IDS[:1]
)
def test_single_load_failures(
    ipath, opts, tmp_path: pathlib.Path
) -> None:
    scm = tmp_path / 'scm.json'
    scm.write_text(SCM_NG_0)

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter('always')
        res = TT.single_load(
            ipath, ac_schema=scm, ac_schema_safe=True, **opts
        )
        assert res is None
        assert len(warns) > 0
        assert issubclass(warns[-1].category, UserWarning)
        assert 'scm=' in str(warns[-1].message)

    with pytest.raises(ValidationError):
        TT.single_load(ipath, ac_schema=scm, ac_schema_safe=False)
