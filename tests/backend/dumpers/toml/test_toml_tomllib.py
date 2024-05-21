#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
"""Test cases for the loader.
"""
import pathlib
import typing

import pytest

import tests.common.tdi_base
import tests.common.dumper


from ... import common

if typing.TYPE_CHECKING:
    import pathlib


try:
    DATA = common.load_data_for_testfile(__file__, load_idata=True)
except FileNotFoundError:
    pytest.skip(
        f"Not found test data for: {__file__}",
        allow_module_level=True
    )

NAMES: tuple[str, ...] = ("ipath", "idata", "opts", "exp")
DATA_IDS: list[str] = common.get_test_ids(DATA)
Parser = getattr(common.get_mod(__file__), "Parser", None)

if Parser is None:
    pytest.skip(
        f"Skip test cases: {__file__}",
        allow_module_level=True
    )


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_dumps(ipath: str, idata, opts: dict, exp: str) -> None:
    psr = Parser()
    content = psr.dumps(idata, **opts)

    assert psr.loads(content, **opts) == idata
    # assert content == exp  # This may fail.


@pytest.mark.parametrize(NAMES, DATA, ids=DATA_IDS)
def test_dump(
    ipath: str, idata, opts: dict, exp: str, tmp_path: pathlib.Path
) -> None:
    psr = Parser()

    opath = tmp_path / f"{ipath.stem}.{psr.extensions()[0]}"
    ioi = common.ioinfo_from_path(opath)

    psr.dump(idata, ioi, **opts)

    assert opath.exists()
    assert psr.load(ioi, **opts) == idata

    content = psr.ropen(str(opath)).read().decode("utf-8")
    # assert content == exp  # This may fail.


class TDI(tests.common.tdi_base.TDI):
    _cid = tests.common.tdi_base.name_from_path(__file__)
    _is_loader = False


(TT, DATA, DATA_IDS) = TDI().get_all()

if TT is None:
    pytest.skip(
        f"skipping tests: {TDI().cid()} as it's not available.",
        allow_module_level=True
    )

assert DATA


class TestCase(tests.common.dumper.TestCase):
    psr_cls = TT.Parser
    exact_match = False

    @pytest.mark.parametrize(
        ("ipath", "aux"), DATA, ids=DATA_IDS,
    )
    def test_dumps(
        self, ipath: pathlib.Path, aux: dict[str, typing.Any],
    ):
        self._assert_dumps(ipath, aux)

    @pytest.mark.parametrize(
        ("ipath", "aux"), DATA, ids=DATA_IDS,
    )
    def test_dump(
        self, ipath: pathlib.Path, aux: dict[str, typing.Any],
        tmp_path: pathlib.Path
    ):
        self._assert_dump(ipath, aux, tmp_path)
