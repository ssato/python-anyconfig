from setuptools import setup, Command, find_packages

import glob
import os.path
import os


curdir = os.getcwd()

PACKAGE = "anyconfig"
VERSION = "0.0.6"  # see anyconfig.globals.VERSION

# For daily snapshot versioning mode:
if os.environ.get("_SNAPSHOT_BUILD", None) is not None:
    import datetime
    VERSION = VERSION + datetime.datetime.now().strftime(".%Y%m%d")


def list_filepaths(tdir):
    return [f for f in glob.glob(os.path.join(tdir, '*')) if os.path.isfile(f)]


data_files = [("share/man/man1", list_filepaths("docs/"))]


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
                os.makedirs(sdir, 493)  # 493 = 0o755 (py3) or 0755 (py2)

        c = open(rpmspec + ".in").read()
        open(rpmspec, "w").write(c.replace("@VERSION@", VERSION))

        os.system(self.cmd_fmt % params)


class RpmCommand(SrpmCommand):

    build_stage = "b"


_CLASSIFIERS = ["Development Status :: 4 - Beta",
                "Intended Audience :: Developers",
                "Programming Language :: Python",
                "Programming Language :: Python :: 2",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 2.6",
                "Programming Language :: Python :: 2.7",
                "Programming Language :: Python :: 3.2",
                "Programming Language :: Python :: 3.3",
                "Programming Language :: Python :: 3.4",
                "Environment :: Console",
                "Operating System :: OS Independent",
                "Topic :: Software Development :: Libraries :: Python Modules",
                "Topic :: Text Processing :: Markup",
                "Topic :: Utilities",
                "License :: OSI Approved :: MIT License"]

TESTS_REQ = [l.rstrip() for l in open("pkg/test_requirements.txt").readlines()
             if l and not l.startswith('#')]


setup(name=PACKAGE,
      version=VERSION,
      description="Generic access to configuration files in some formats",
      long_description=open("README.rst").read(),
      author="Satoru SATOH",
      author_email="ssato@redhat.com",
      license="MIT",
      url="https://github.com/ssato/python-anyconfig",
      classifiers=_CLASSIFIERS,
      tests_require=TESTS_REQ,
      packages=find_packages(),
      include_package_data=True,
      cmdclass={
          "srpm": SrpmCommand,
          "rpm":  RpmCommand,
      },
      entry_points=open(os.path.join(curdir, "pkg/entry_points.txt")).read(),
      data_files=data_files,
      )

# vim:sw=4:ts=4:et:
