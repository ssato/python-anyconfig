#
# Copyright (C) 2015 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
from __future__ import annotations

import os
import pathlib
import unittest.mock

import pytest

try:
    import anyconfig.template.jinja2 as TT
except ImportError:
    pytest.skip(
        "jinja2 does not look available.",
        allow_module_level=True
    )

from .. import common


TDATA_DIR = common.RESOURCE_DIR / "templates" / "jinja2"

TEMPLATES = [
    (p, r.read_text()) for p, r in (
        (path, (TDATA_DIR / "10" / "r" / f"{path.stem}.txt"))
        for path in (TDATA_DIR / "10").glob("*.j2")
    ) if r.exists()
]

TEMPLATES_WITH_FILTERS = [
    (p, r.read_text()) for p, r in (
        (path, (TDATA_DIR / "20" / "r" / f"{path.stem}.txt"))
        for path in (TDATA_DIR / "20").glob("*.j2")
    ) if r.exists()
]

assert TEMPLATES
assert TEMPLATES_WITH_FILTERS


def normalize(txt: str):
    """Strip white spaces and line break at the end of the content ``txt``.
    """
    return txt.strip().rstrip()


def negate(value):
    return - value


TMPL_DIR_10 = pathlib.Path("/path/to/a/").resolve()
TMPL_PATH_10 = TMPL_DIR_10 / "tmpl.j2"
TMP_DIR = pathlib.Path("/tmp").resolve()


@pytest.mark.parametrize(
    ("args", "exp"),
    (((TMPL_PATH_10, ), [TMPL_DIR_10]),
     ((TMPL_PATH_10, [TMP_DIR]), [TMPL_DIR_10, TMP_DIR]),
     ),
)
def test_make_template_paths(args, exp):
    assert TT.make_template_paths(*args) == exp


def test_make_template_paths_after_chdir(tmp_path):
    old_pwd = pathlib.Path().cwd().resolve()
    path_1 = tmp_path / "t.j2"

    try:
        os.chdir(str(tmp_path))

        assert TT.make_template_paths(path_1) == [tmp_path]
        assert TT.make_template_paths(path_1, [tmp_path]) == [tmp_path]
    except FileNotFoundError:
        pass  # ``tmp0`` does not exist on windows.
    finally:
        os.chdir(str(old_pwd))


def __assert_almost_eq(lhs, rhs):
    assert normalize(lhs) == normalize(rhs)


@pytest.mark.parametrize(("tmpl", "exp"), TEMPLATES)
def test_render_impl_without_paths(tmpl, exp):
    __assert_almost_eq(TT.render_impl(tmpl), exp)


@pytest.mark.parametrize(("tmpl", "exp"), TEMPLATES)
def test_render_impl_with_paths(tmpl, exp):
    __assert_almost_eq(TT.render_impl(tmpl, paths=[tmpl.parent]), exp)


@pytest.mark.parametrize(("tmpl", "exp"), TEMPLATES)
def test_render_without_paths(tmpl, exp):
    __assert_almost_eq(TT.render(tmpl), exp)


def test_try_render_with_empty_filepath_and_content():
    with pytest.raises(ValueError):
        TT.try_render()


@pytest.mark.parametrize(("tmpl", "exp"), TEMPLATES_WITH_FILTERS)
def test_render_with_filter(tmpl, exp):
    __assert_almost_eq(TT.render(tmpl, filters={"negate": negate}), exp)


def test_render_with_wrong_path(tmp_path):
    workdir = tmp_path

    ng_t = workdir / "ng.j2"
    ok_t = workdir / "ok.j2"
    ok_t_content = "a: {{ a }}"
    ok_content = "a: aaa"
    ctx = {"a": "aaa"}

    ok_t.write_text(ok_t_content)

    with unittest.mock.patch("builtins.input") as mock_input:
        mock_input.return_value = str(ok_t)
        assert TT.render(str(ng_t), ctx, ask=True) == ok_content

    with pytest.raises(TT.jinja2.TemplateNotFound):
        TT.render(str(ng_t), ctx, ask=False)
