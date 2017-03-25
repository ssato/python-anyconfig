#
# Copyright (C) 2015 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, unused-variable
import os.path
import os
import unittest
import mock

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


class Test(unittest.TestCase):

    templates = TMPLS

    def setUp(self):
        self.workdir = tests.common.setup_workdir()
        for fname, tmpl_s, _ctx in self.templates:
            fpath = os.path.join(self.workdir, fname)
            open(fpath, 'w').write(tmpl_s)

    def tearDown(self):
        tests.common.cleanup_workdir(self.workdir)

    def test_10_render_impl__wo_paths(self):
        if TT.SUPPORTED:
            for fname, _str, ctx in self.templates:
                fpath = os.path.join(self.workdir, fname)
                c_r = TT.render_impl(fpath)
                self.assertEqual(c_r, ctx)

    def test_12_render_impl__w_paths(self):
        if TT.SUPPORTED:
            for fname, _str, ctx in self.templates:
                fpath = os.path.join(self.workdir, fname)
                c_r = TT.render_impl(os.path.basename(fpath),
                                     paths=[os.path.dirname(fpath)])
                self.assertEqual(c_r, ctx)

    def test_20_render__wo_paths(self):
        if TT.SUPPORTED:
            for fname, _str, ctx in self.templates:
                fpath = os.path.join(self.workdir, fname)
                c_r = TT.render(fpath)
                self.assertEqual(c_r, ctx)

    def test_22_render__w_wrong_tpath(self):
        if TT.SUPPORTED:
            mpt = "anyconfig.compat.raw_input"

            ng_t = os.path.join(self.workdir, "ng.j2")
            ok_t = os.path.join(self.workdir, "ok.j2")
            ok_t_content = "a: {{ a }}"
            ok_content = "a: aaa"
            ctx = dict(a="aaa", )

            open(ok_t, 'w').write(ok_t_content)

            with mock.patch(mpt, return_value=ok_t):
                c_r = TT.render(ng_t, ctx, ask=True)
                self.assertEqual(c_r, ok_content)
            try:
                TT.render(ng_t, ctx, ask=False)
                assert False  # force raising an exception.
            except TT.TemplateNotFound:
                pass

    def test_24_render__wo_paths(self):
        if TT.SUPPORTED:
            fname = self.templates[0][0]
            assert os.path.exists(os.path.join(self.workdir, fname))

            subdir = os.path.join(self.workdir, "a/b/c")
            os.makedirs(subdir)

            tmpl = os.path.join(subdir, fname)
            open(tmpl, 'w').write("{{ a|default('aaa') }}")

            c_r = TT.render(tmpl)
            self.assertEqual(c_r, "aaa")

    def test_25_render__w_prefer_paths(self):
        if TT.SUPPORTED:
            fname = self.templates[0][0]
            assert os.path.exists(os.path.join(self.workdir, fname))

            subdir = os.path.join(self.workdir, "a/b/c")
            os.makedirs(subdir)

            tmpl = os.path.join(subdir, fname)
            open(tmpl, 'w').write("{{ a|default('aaa') }}")

            c_r = TT.render(tmpl, paths=[self.workdir])
            self.assertNotEqual(c_r, "aaa")
            self.assertEqual(c_r, self.templates[0][-1])

    def test_30_try_render_with_empty_filepath_and_content(self):
        if TT.SUPPORTED:
            try:
                TT.try_render()
            except ValueError:
                exc_was_raised = True
            self.assertTrue(exc_was_raised)

# vim:sw=4:ts=4:et:
