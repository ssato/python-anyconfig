from distutils.core import setup, Command

import datetime
import glob
import os
import sys

curdir = os.getcwd()
sys.path.append(curdir)

import anyconfig

PACKAGE = "anyconfig"
VERSION = anyconfig.VERSION

data_files = []


class SrpmCommand(Command):

    user_options = []

    build_stage = "s"
    cmd_fmt = """rpmbuild -b%(build_stage)s \
        --define \"_topdir %(rpmdir)s\" \
        --define \"_sourcedir %(rpmdir)s\" \
        --define \"_buildroot %(BUILDROOT)s\" \
        %(rpmspec)s
    """

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('sdist')
        self.build_rpm()

    def build_rpm(self):
        params = dict()

        params["build_stage"] = self.build_stage
        rpmdir = params["rpmdir"] = os.path.join(
            os.path.abspath(os.curdir), "dist"
        )
        rpmspec = params["rpmspec"] = os.path.join(
            rpmdir, "../python-%s.spec" % PACKAGE
        )

        for subdir in ("SRPMS", "RPMS", "BUILD", "BUILDROOT"):
            sdir = params[subdir] = os.path.join(rpmdir, subdir)

            if not os.path.exists(sdir):
                os.makedirs(sdir, 0755)

        c = open(rpmspec + ".in").read()
        open(rpmspec, "w").write(c.replace("@VERSION@", VERSION))

        os.system(self.cmd_fmt % params)


class RpmCommand(SrpmCommand):

    build_stage = "b"


setup(name=PACKAGE,
    version=VERSION,
    description="Generic access to configuration files in some formats",
    long_description=open("README.rst").read(),
    author="Satoru SATOH",
    author_email="ssato@redhat.com",
    license="MIT",
    url="https://github.com/ssato/python-anyconfig",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    #platform=
    #install_requires=[],
    #tests_require=['nose', 'pep8'],
    packages=[
        "anyconfig",
        "anyconfig.tests",
        "anyconfig.backend",
        "anyconfig.backend.tests",
    ],
    scripts=glob.glob("src/*"),
    data_files=data_files,
    cmdclass={
        "srpm": SrpmCommand,
        "rpm":  RpmCommand,
    },
)

# vim:sw=4:ts=4:et:
