from setuptools import setup, Command, find_packages

import glob
import os.path
import os
import subprocess


PACKAGE = "m9dicts"
VERSION = "0.2.0"  # see m9dicts.__version__

# For daily snapshot versioning mode:
if os.environ.get("_SNAPSHOT_BUILD", None) is not None:
    import datetime
    VERSION = VERSION + datetime.datetime.now().strftime(".%Y%m%d")


_LONG_DESC = """
python-m9dicts (merge-able dicts) is a `MIT licensed
<http://opensource.org/licenses/MIT>`_ python library provides some dict-like
objects support recursive merge operations according to each merge strategies.

- Home: https://github.com/ssato/python-m9dicts
- PyPI: https://pypi.python.org/pypi/m9dicts
"""


class SrpmCommand(Command):

    user_options = []
    build_stage = "s"

    curdir = os.path.abspath(os.curdir)
    rpmspec = os.path.join(curdir, "pkg/package.spec")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.pre_sdist()
        self.run_command('sdist')
        self.build_rpm()

    def pre_sdist(self):
        c = open(self.rpmspec + ".in").read()
        open(self.rpmspec, "w").write(c.replace("@VERSION@", VERSION))

    def build_rpm(self):
        rpmbuild = os.path.join(self.curdir, "pkg/rpmbuild-wrapper.sh")
        workdir = os.path.join(self.curdir, "dist")

        cmd_s = "%s -w %s -s %s %s" % (rpmbuild, workdir, self.build_stage,
                                       self.rpmspec)
        subprocess.check_call(cmd_s, shell=True)


class RpmCommand(SrpmCommand):

    build_stage = "b"


_CLASSIFIERS = ["Development Status :: 4 - Beta",
                "Intended Audience :: Developers",
                "Programming Language :: Python",
                "Programming Language :: Python :: 2",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 2.6",
                "Programming Language :: Python :: 2.7",
                "Programming Language :: Python :: 3.3",
                "Programming Language :: Python :: 3.4",
                "Programming Language :: Python :: 3.5",
                "Environment :: Console",
                "Operating System :: OS Independent",
                "Topic :: Software Development :: Libraries",
                "Topic :: Software Development :: Libraries :: Python Modules",
                "Topic :: Utilities",
                "License :: OSI Approved :: MIT License"]


setup(name=PACKAGE,
      version=VERSION,
      description="dict-like objects support recursive merge operations",
      long_description=_LONG_DESC,
      author="Satoru SATOH",
      author_email="ssato@redhat.com",
      license="MIT",
      url="https://github.com/ssato/python-m9dicts",
      classifiers=_CLASSIFIERS,
      packages=find_packages(),
      include_package_data=True,
      cmdclass={
          "srpm": SrpmCommand,
          "rpm":  RpmCommand,
      },
      )

# vim:sw=4:ts=4:et:
