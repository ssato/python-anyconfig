"""setup.py to build package.
"""
from __future__ import absolute_import

import glob
import os.path
import os
import re
import setuptools
import setuptools.command.bdist_rpm


# It might throw IndexError and so on.
VERSION = [re.search(r'^VERSION = "([^"]+)"', l).groups()[0] for l
           in open(glob.glob("src/*/globals.py")[0])
           if "VERSION" in l][0]

# For daily snapshot versioning mode:
RELEASE = "1%{?dist}"
if os.environ.get("_SNAPSHOT_BUILD", None) is not None:
    import datetime
    RELEASE = RELEASE.replace('1',
                              datetime.datetime.now().strftime(".%Y%m%d"))


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
    spec_tmpl = os.path.join(os.path.abspath(os.curdir),
                             "pkg/package.spec.in")

    def _make_spec_file(self):
        return [_replace(l.rstrip()) for l in open(self.spec_tmpl)]


setuptools.setup(name="anyconfig",   # Avoid 'Unknown' package in older ones.
                 version=VERSION,
                 cmdclass=dict(bdist_rpm=bdist_rpm),
                 package_dir={'': 'src'},
                 data_files=[("share/man/man1", ["docs/anyconfig_cli.1"])])

# vim:sw=4:ts=4:et:
