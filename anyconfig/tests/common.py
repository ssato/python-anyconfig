#
# Copyright (C) 2011 - 2014 Satoru SATOH <ssato at redhat.com>
#
import imp
import os.path
import sys
import tempfile


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
        if fullname in self.masked:
            return self
        return None

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

# vim:sw=4:ts=4:et:
