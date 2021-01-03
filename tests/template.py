#
# Copyright (C) 2015 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, unused-variable, invalid-name
import os
import pathlib
import unittest
import unittest.mock

import anyconfig.template as TT
import tests.common


C_1 = """A char is 'a'.
A char is 'b'.
A char is 'c'.
"""

TMPLS = [('00.j2', "{% include '10.j2' %}" + os.linesep, C_1),
         ('10.j2', """{% for c in ['a', 'b', 'c'] -%}
A char is '{{ c }}'.
{% endfor %}
""", C_1)]

C_2 = "-1"
TMPL_WITH_FILTER = ('11.j2', "{{ 1|negate }}", C_2)


def negate(value):
    return -value


@unittest.skipIf(not TT.SUPPORTED, 'Template library is not available.')
class TestCase(tests.common.TestCaseWithWorkdir):

    templates = TMPLS

    def setUp(self):
        super().setUp()
        for fname, tmpl_s, _ctx in self.templates + [TMPL_WITH_FILTER]:
            (pathlib.Path(self.workdir) / fname).write_text(tmpl_s)

    def test_10_render_impl__wo_paths(self):
        for fname, _str, ctx in self.templates:
            fpath = pathlib.Path(self.workdir) / fname
            c_r = TT.render_impl(str(fpath))
            self.assertEqual(c_r, ctx)

    def test_12_render_impl__w_paths(self):
        for fname, _str, ctx in self.templates:
            fpath = pathlib.Path(self.workdir) / fname
            c_r = TT.render_impl(fpath.name, paths=[self.workdir])
            self.assertEqual(c_r, ctx)

    def test_20_render__wo_paths(self):
        for fname, _str, ctx in self.templates:
            fpath = pathlib.Path(self.workdir) / fname
            c_r = TT.render(str(fpath))
            self.assertEqual(c_r, ctx)

    def test_22_render__w_wrong_tpath(self):
        ng_t = pathlib.Path(self.workdir) / "ng.j2"
        ok_t = pathlib.Path(self.workdir) / "ok.j2"
        ok_t_content = "a: {{ a }}"
        ok_content = "a: aaa"
        ctx = dict(a="aaa", )

        ok_t.write_text(ok_t_content)

        with unittest.mock.patch("builtins.input") as mock_input:
            mock_input.return_value = str(ok_t)
            c_r = TT.render(str(ng_t), ctx, ask=True)
            self.assertEqual(c_r, ok_content)
        try:
            TT.render(str(ng_t), ctx, ask=False)
            assert False  # force raising an exception.
        except TT.TemplateNotFound:
            pass

    def test_24_render__wo_paths(self):
        if TT.SUPPORTED:
            fname = self.templates[0][0]
            workdir = pathlib.Path(self.workdir)

            assert workdir / fname

            subdir = workdir / "a/b/c"
            subdir.mkdir(parents=True)

            tmpl = subdir / fname
            tmpl.write_text("{{ a|default('aaa') }}")

            c_r = TT.render(str(tmpl))
            self.assertEqual(c_r, "aaa")

    def test_25_render__w_prefer_paths(self):
        workdir = pathlib.Path(self.workdir / 'a' / 'b' / 'c')
        workdir.mkdir(parents=True)

        assert workdir.exists()

        tmpl_ref = pathlib.Path(self.workdir / 'ref_25_0.j2')
        tmpl_ref.write_text("{{ a | d('A') }}\n")

        tmpl = pathlib.Path(workdir / 'd.j2')
        tmpl.write_text("{{ a | d('xyz') }}\n")

        c_r = TT.render(tmpl, paths=[self.workdir])
        self.assertNotEqual(c_r, 'A')
        self.assertEqual(c_r, 'xyz')

    def test_30_try_render_with_empty_filepath_and_content(self):
        self.assertRaises(ValueError, TT.try_render)

    def test_40_render__w_filter(self):
        fname, _, ctx = TMPL_WITH_FILTER
        fpath = pathlib.Path(self.workdir) / fname
        c_r = TT.render(str(fpath), filters={"negate": negate})
        self.assertEqual(c_r, ctx)

# vim:sw=4:ts=4:et:
