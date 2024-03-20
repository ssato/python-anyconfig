#
# Copyright (C) 2015 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, unused-variable, invalid-name
import os
import pathlib
import tempfile
import unittest
import unittest.mock

try:
    import anyconfig.template.jinja2 as TT
except ImportError:
    raise unittest.SkipTest("jinja2 does not look available.")

from .. import base


TDATA_DIR = base.RES_DIR / "template/jinja2/"

TEMPLATES = [
    (path, (TDATA_DIR / "10/r/10.txt").read_text())
    for path in (TDATA_DIR / "10").glob("*.j2")
]
TEMPLATES_WITH_FILTERS = [
    (path, (TDATA_DIR / f"20/r/{path.stem}.txt").read_text())
    for path in (TDATA_DIR / "20").glob("*.j2")
]


def normalize(txt: str):
    """Strip white spaces and line break at the end of the content ``txt``.
    """
    return txt.strip().rstrip()


def negate(value):
    return - value


class FunctionsTestCase(unittest.TestCase):

    def test_make_template_paths(self):
        tpath0 = pathlib.Path("/path/to/a/").resolve()
        path0 = tpath0 / "tmpl.j2"
        tmp0 = pathlib.Path("/tmp").resolve()
        ies = (((path0, ), [tpath0]),
               ((path0, [tmp0]), [tpath0, tmp0]),
               )
        for inp, exp in ies:
            self.assertEqual(
                TT.make_template_paths(*inp), exp
            )

    def test_make_template_paths_after_chdir(self):
        tmp0 = pathlib.Path("/tmp").resolve()
        saved = pathlib.Path().cwd().resolve()
        try:
            os.chdir(str(tmp0))
            tpath1 = pathlib.Path(".")
            path1 = tpath1 / "tmpl.j2"
            ies = (((path1, ), [tmp0]),
                   ((path1, [tmp0]), [tmp0]),
                   )

            for inp, exp in ies:
                self.assertEqual(
                    TT.make_template_paths(*inp), exp
                )
        except FileNotFoundError:
            pass  # ``tmp0`` does not exist on windows.
        finally:
            os.chdir(str(saved))


class TestCase(unittest.TestCase):

    def assertAlmostEqual(self, inp, exp, **_kwargs):
        """Override to allow to compare texts.
        """
        self.assertEqual(normalize(inp), normalize(exp))

    def test_render_impl_without_paths(self):
        for inp, exp in TEMPLATES:
            self.assertAlmostEqual(TT.render_impl(inp), exp)

    def test_render_impl_with_paths(self):
        for inp, exp in TEMPLATES:
            self.assertAlmostEqual(
                TT.render_impl(inp, paths=[inp.parent]), exp
            )

    def test_render_without_paths(self):
        for inp, exp in TEMPLATES:
            self.assertAlmostEqual(TT.render(inp), exp)

    def test_render_with_wrong_path(self):
        with tempfile.TemporaryDirectory() as tdir:
            workdir = pathlib.Path(tdir)

            ng_t = workdir / "ng.j2"
            ok_t = workdir / "ok.j2"
            ok_t_content = "a: {{ a }}"
            ok_content = "a: aaa"
            ctx = dict(a="aaa", )

            ok_t.write_text(ok_t_content)

            with unittest.mock.patch("builtins.input") as mock_input:
                mock_input.return_value = str(ok_t)
                c_r = TT.render(str(ng_t), ctx, ask=True)
                self.assertEqual(c_r, ok_content)

            with self.assertRaises(TT.jinja2.TemplateNotFound):
                TT.render(str(ng_t), ctx, ask=False)

    def test_try_render_with_empty_filepath_and_content(self):
        self.assertRaises(ValueError, TT.try_render)

    def test_render_with_filter(self):
        for inp, exp in TEMPLATES_WITH_FILTERS:
            self.assertAlmostEqual(
                TT.render(inp, filters={"negate": negate}), exp
            )

# vim:sw=4:ts=4:et:
