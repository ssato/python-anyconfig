#
# Copyright (C) 2015 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
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

NULL_DEV = "/dev/null"
if not pathlib.Path(NULL_DEV).exists():
    NULL_DEV = "NUL"


def check_output(cmd):
    devnull = open(NULL_DEV, "w")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=devnull)
    return proc.communicate()[0]


class TestCase(unittest.TestCase):

    def test_00_run_script(self):
        with tempfile.TemporaryDirectory(prefix="anyconfig-tests-") as tmpdir:
            script = pathlib.Path(tmpdir) / "a.py"
            script.write_text(SCRIPT_TO_USE_ANYCONFIG)

            out = check_output(["python", str(script)])
            self.assertTrue(out in (b"", ""))

# vim:sw=4:ts=4:et:
