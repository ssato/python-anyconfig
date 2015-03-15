#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import os.path
import mock
import unittest

import anyconfig.template as TT
import anyconfig.tests.common


C_1 = """A char is 'a'.
A char is 'b'.
A char is 'c'.
"""

TMPLS = [('00.j2', "{% include '10.j2' %}\n", C_1),
         ('10.j2', """{% for c in ['a', 'b', 'c'] -%}
A char is '{{ c }}'.
{% endfor %}
""", C_1)]


class Test_20_render_templates(unittest.TestCase):

    templates = TMPLS

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()
        for fn, tmpl_s, _c in self.templates:
            f = os.path.join(self.workdir, fn)
            open(f, 'w').write(tmpl_s)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_render_impl__wo_paths(self):
        if TT.TEMPLATE_SUPPORT:
            for fn, _s, c in self.templates:
                f = os.path.join(self.workdir, fn)
                c_r = TT.render_impl(f)
                self.assertEquals(c_r, c)

    def test_12_render_impl__w_paths(self):
        if TT.TEMPLATE_SUPPORT:
            for fn, _s, c in self.templates:
                f = os.path.join(self.workdir, fn)
                c_r = TT.render_impl(os.path.basename(f),
                                     paths=[os.path.dirname(f)])
                self.assertEquals(c_r, c)

    def test_20_render__wo_paths(self):
        if TT.TEMPLATE_SUPPORT:
            for fn, _s, c in self.templates:
                f = os.path.join(self.workdir, fn)
                c_r = TT.render(f)
                self.assertEquals(c_r, c)

    def test_22_render__w_wrong_template_path(self):
        if TT.TEMPLATE_SUPPORT:
            mpt = "anyconfig.compat.raw_input"

            ng_t = os.path.join(self.workdir, "ng.j2")
            ok_t = os.path.join(self.workdir, "ok.j2")
            ok_t_content = "a: {{ a }}"
            ok_content = "a: aaa"
            ctx = dict(a="aaa", )

            open(ok_t, 'w').write(ok_t_content)

            with mock.patch(mpt, return_value=ok_t):
                c_r = TT.render(ng_t, ctx, ask=True)
                self.assertEquals(c_r, ok_content)

# vim:sw=4:ts=4:et:
