#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato at redhat.com>
#
import os.path
import tempfile


def selfdir():
    return os.path.dirname(__file__)


def setup_workdir():
    return tempfile.mkdtemp(dir="/tmp", prefix="anyconfig-tests")


def cleanup_workdir(workdir):
    """
    FIXME: Danger!
    """
    os.system("rm -rf " + workdir)


# vim:sw=4:ts=4:et:
