#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.template as TT
import anyconfig.tests.common as C

import os.path
import unittest


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
        self.workdir = C.setup_workdir()
        for fn, tmpl_s, _c in self.templates:
            f = os.path.join(self.workdir, fn)
            open(f, 'w').write(tmpl_s)

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

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

# vim:sw=4:ts=4:et:
