"""setup.py to build package.
"""
from __future__ import absolute_import

import os
import pathlib
import re
import setuptools
import setuptools.command.bdist_rpm


# It might throw IndexError and so on.
VERSION = '0.1.0'
VER_REG = re.compile(r'^__version__ = "([^"]+)"')

for fpath in pathlib.Path('src').glob('*/*.py'):
    for line in fpath.open():
        match = VER_REG.match(line)
        if match:
            VERSION = match.groups()[0]
            break

# For daily snapshot versioning mode:
RELEASE = "1%{?dist}"
if os.environ.get("_SNAPSHOT_BUILD", None) is not None:
    import datetime
    RELEASE = RELEASE.replace('1',
                              datetime.datetime.now().strftime("%Y%m%d"))


def _replace(line):
    """Replace some strings in the RPM SPEC template"""
    if "@VERSION@" in line:
        return line.replace("@VERSION@", VERSION)

    if "@RELEASE@" in line:
        return line.replace("@RELEASE@", RELEASE)

    if "Source0:" in line:  # Dirty hack
        return "Source0: %{pkgname}-%{version}.tar.gz"

    return line


class bdist_rpm(setuptools.command.bdist_rpm.bdist_rpm):
    """Override the default content of the RPM SPEC.
    """
    spec_tmpl = pathlib.Path('pkg/package.spec.in').resolve()

    def _make_spec_file(self):
        return [_replace(line.rstrip()) for line in self.spec_tmpl.open()]


setuptools.setup(version=VERSION, cmdclass=dict(bdist_rpm=bdist_rpm),
                 data_files=[("share/man/man1", ["docs/anyconfig_cli.1"])])

# vim:sw=4:ts=4:et:
