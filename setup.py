from __future__ import absolute_import

import os.path
import os
import sys
import setuptools
import setuptools.command.bdist_rpm

sys.path.insert(0, os.path.dirname(__file__))  # load anyconfig from this dir.

from anyconfig.globals import VERSION


# For daily snapshot versioning mode:
if os.environ.get("_SNAPSHOT_BUILD", None) is not None:
    import datetime
    VERSION = VERSION + datetime.datetime.now().strftime(".%Y%m%d")


class bdist_rpm(setuptools.command.bdist_rpm.bdist_rpm):
    """Override the default content of the RPM SPEC.
    """
    spec_tmpl = os.path.join(os.path.abspath(os.curdir),
                             "pkg/package.spec.in")

    def _replace(self, line):
        """Replace some strings in the RPM SPEC template"""
        if "@VERSION@" in line:
            return line.replace("@VERSION@", VERSION)

        if "Source0:" in line:  # Dirty hack
            return "Source0: %{pkgname}-%{version}.tar.gz"

        return line

    def _make_spec_file(self):
        return [self._replace(l.rstrip()) for l
                in open(self.spec_tmpl).readlines()]


setuptools.setup(version=VERSION,
                 cmdclass=dict(bdist_rpm=bdist_rpm),
                 data_files=[("share/man/man1", ["docs/anyconfig_cli.1"])])

# vim:sw=4:ts=4:et:
