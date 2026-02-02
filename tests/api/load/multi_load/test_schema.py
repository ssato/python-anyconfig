#
# Copyright (C) 2021 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.api.load with schema validation."""
from __future__ import annotations

import typing

import pytest

import anyconfig.api._load as TT
import anyconfig.schema

from anyconfig.api import ValidationError

from . import common

if typing.TYPE_CHECKING:
    import pathlib


if "jsonschema" not in anyconfig.schema.VALIDATORS:
    pytest.skip(
        "jsonschema lib is not available.",
        allow_module_level=True,
    )


def scm_path_from_inputs(inputs: list[pathlib.Path]) -> pathlib.Path:
    path = inputs[0]
    name = path.name[:-len(path.suffix)]
    return next((path.parent / "s").glob(f"{name}.*"))


NAMES: tuple[str, ...] = (*common.NAMES, "scm")
DATA = [
    (inputs, *rest, scm_path_from_inputs(inputs))
    for inputs, *rest in common.load_data_for_testfile(__file__)
]
DATA_IDS: list[str] = common.get_test_ids(DATA)


def test_data() -> None:
    assert DATA


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_load(
    inputs: list[pathlib.Path], opts: dict, exp, scm: pathlib.Path,
) -> None:
    assert TT.load(inputs, ac_schema=scm, **opts) == exp


SCM_NG_0 = '{"type": "object", "properties": {"a": {"type": "string"}}}'


@pytest.mark.parametrize(NAMES, DATA[:1], ids=DATA_IDS[:1])
def test_load_with_validation_failure(
    inputs: list[pathlib.Path], opts: dict, exp, scm: pathlib.Path,
    tmp_path: pathlib.Path,
) -> None:
    assert exp or scm  # dummy

    scm = tmp_path / "scm.json"
    scm.write_text(SCM_NG_0)

    with pytest.raises(ValidationError):
        TT.load(
            inputs, ac_schema=scm, ac_schema_safe=False, **opts,
        )
