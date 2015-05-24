#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato at redhat.com>
#
# pylint: disable=missing-docstring
import imp
import os.path
import sys
import tempfile
import unittest


def selfdir():
    return os.path.dirname(__file__)


def setup_workdir():
    return tempfile.mkdtemp(dir="/tmp", prefix="python-anyconfig-tests-")


def cleanup_workdir(workdir):
    """
    FIXME: Danger!
    """
    os.system("rm -rf " + workdir)


class MaskedImportLoader(object):
    """
    Mask specified module[s] and block importing that module / these modules to
    raise ImportError on purpose.

    see also: http://pymotw.com/2/sys/imports.html
    """

    def __init__(self, *modules):
        """
        :param modules: A list of name of modules to mask
        """
        self.masked = modules

    def find_module(self, fullname, path=None):
        return self if fullname in self.masked else None

    def load_module(self, fullname):
        """
        :param fullname: Full name of the module to load
        """
        if fullname in self.masked:
            raise ImportError("Could not import %s as it's masked" % fullname)

        # Stallen from NoisyMetaImportLoader.load_module.
        if fullname in sys.modules:
            mod = sys.modules[fullname]
        else:
            mod = sys.modules.setdefault(fullname, imp.new_module(fullname))

        # Set a few properties required by PEP 302
        mod.__file__ = fullname
        mod.__name__ = fullname
        mod.__loader__ = self
        mod.__package__ = '.'.join(fullname.split('.')[:-1])

        return mod


def mask_modules(*modules):
    sys.meta_path.append(MaskedImportLoader(*modules))


class Test_00_MaskedImportLoader(unittest.TestCase):

    def test_00___init__(self):
        ms = ("lxml", "yaml", "json")
        mil = MaskedImportLoader(*ms)
        self.assertEquals(mil.masked, ms)

    def test_10_find_module(self):
        mil = MaskedImportLoader("lxml", "yaml")
        self.assertTrue(mil.find_module("lxml.etree") is None)

    def test_20_load_module__basename(self):
        mod = None
        mil = MaskedImportLoader("platform")

        try:
            mod = mil.load_module("platform")
        except ImportError:
            pass

        self.assertTrue(mod is None)

    def test_22_load_module__fullname(self):
        mod = None
        mil = MaskedImportLoader("logging.config")

        try:
            mod = mil.load_module("logging.config")
        except ImportError:
            pass

        self.assertTrue(mod is None)

    def test_30_mask_modules__a_module(self):
        """
        TODO: Implement it correctly and add a test case.

        collections = None
        mask_modules("collections")

        try:
            import collections
        except ImportError:
            pass

        self.assertTrue(collections is None)
        """
        pass

# vim:sw=4:ts=4:et:
