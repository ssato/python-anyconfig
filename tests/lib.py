#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import pathlib
import subprocess
import tempfile
import unittest


SCRIPT_TO_USE_ANYCONFIG = """\
#! /usr/bin/env python
import anyconfig

c = anyconfig.load("/") or {}
anyconfig.dump(c, "/dev/null", "yaml")
"""


def check_output(cmd):
    devnull = open('/dev/null', 'w')
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=devnull)
    return proc.communicate()[0]


class TestCase(unittest.TestCase):

    def test_00_run_script(self):
        with tempfile.TemporaryDirectory(prefix='anyconfig-tests-') as tmpdir:
            script = pathlib.Path(tmpdir) / "a.py"
            script.write_text(SCRIPT_TO_USE_ANYCONFIG)

            out = check_output(["python", str(script)])
            self.assertTrue(out in (b'', ''))

# vim:sw=4:ts=4:et:
