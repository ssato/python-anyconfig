from __future__ import absolute_import
from setuptools import setup, Command

import glob
import os.path
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))  # load anyconfig from this dir.

from anyconfig.globals import PACKAGE, VERSION


# For daily snapshot versioning mode:
if os.environ.get("_SNAPSHOT_BUILD", None) is not None:
    import datetime
    VERSION = VERSION + datetime.datetime.now().strftime(".%Y%m%d")


def list_filepaths(tdir):
    return [f for f in glob.glob(os.path.join(tdir, '*')) if os.path.isfile(f)]


# TBD:
# data_files = [("share/man/man1", list_filepaths("docs/"))]
data_files = [("share/man/man1", ["docs/anyconfig_cli.1"])]


class SrpmCommand(Command):

    user_options = []
    build_stage = "s"

    curdir = os.path.abspath(os.curdir)
    rpmspec = os.path.join(curdir, "pkg/package.spec")
    gen_readme = os.path.join(curdir, "pkg/gen-readme.sh")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.pre_sdist()
        self.run_command('sdist')
        # Dirty hack.
        self.copy_file("dist/%s-%s.tar.gz" % (PACKAGE, VERSION),
                       "dist/RELEASE_%s.tar.gz" % VERSION)
        self.build_rpm()

    def pre_sdist(self):
        c = open(self.rpmspec + ".in").read()
        open(self.rpmspec, "w").write(c.replace("@VERSION@", VERSION))
        subprocess.check_call(self.gen_readme, shell=True)

    def build_rpm(self):
        rpmbuild = os.path.join(self.curdir, "pkg/rpmbuild-wrapper.sh")
        workdir = os.path.join(self.curdir, "dist")

        cmd_s = "%s -w %s -s %s %s" % (rpmbuild, workdir, self.build_stage,
                                       self.rpmspec)
        subprocess.check_call(cmd_s, shell=True)


class RpmCommand(SrpmCommand):

    build_stage = "b"


setup(name=PACKAGE,
      version=VERSION,
      include_package_data=True,
      cmdclass={
          "srpm": SrpmCommand,
          "rpm":  RpmCommand,
      },
      entry_points=open(os.path.join(os.curdir,
                                     "pkg/entry_points.txt")).read(),
      data_files=data_files)

# vim:sw=4:ts=4:et:
