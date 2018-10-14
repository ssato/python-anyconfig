#
# Copyright (C) 2011 - 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Suppress: import positions after some globals are defined
# pylint: disable=wrong-import-position
"""A module to aggregate config parser (loader/dumper) backends.
"""
from __future__ import absolute_import

import logging

import anyconfig.compat
import anyconfig.ioinfo
import anyconfig.processors
import anyconfig.singleton
import anyconfig.utils

import anyconfig.backend.base
import anyconfig.backend.ini
import anyconfig.backend.json
import anyconfig.backend.pickle
import anyconfig.backend.properties
import anyconfig.backend.shellvars
import anyconfig.backend.xml


LOGGER = logging.getLogger(__name__)
PARSERS = [anyconfig.backend.ini.Parser, anyconfig.backend.json.Parser,
           anyconfig.backend.pickle.Parser,
           anyconfig.backend.properties.Parser,
           anyconfig.backend.shellvars.Parser, anyconfig.backend.xml.Parser]

_NA_MSG = "%s is not available. Disabled %s support."

try:
    import anyconfig.backend.yaml
    PARSERS.append(anyconfig.backend.yaml.Parser)
except ImportError:
    LOGGER.info(_NA_MSG, "yaml module", "YAML")

try:
    import anyconfig.backend.configobj
    PARSERS.append(anyconfig.backend.configobj.Parser)
except ImportError:
    LOGGER.info(_NA_MSG, "ConfigObj module", "its")

try:
    import anyconfig.backend.toml
    PARSERS.append(anyconfig.backend.toml.Parser)
except ImportError:
    LOGGER.info(_NA_MSG, "toml module", "TOML")


class Parsers(anyconfig.processors.Processors,
              anyconfig.singleton.Singleton):
    """
    Manager class for parsers.
    """
    _pgroup = "anyconfig_backends"

    def __init__(self, processors=None):
        """Initialize with PARSERS.
        """
        if processors is None:
            processors = PARSERS

        super(Parsers, self).__init__(processors)

    def find_by_type(self, ptype):
        """Find appropriate parser object to process data of given type.

        :param ptype: Forced parser type or parser class or its instance

        :return: An instance of :class:`~anyconfig.backend.base.Parser`
        :raises: UnknownProcessorTypeError
        """
        if ptype is None or not ptype:
            raise ValueError("The first arguemnt 'ptype' must be a string "
                             "or Parser class or Parser instance")

        return super(Parsers, self).find_by_type(ptype)

    def find(self, obj, forced_type=None,
             cls=anyconfig.models.processor.Processor):
        """Find appropriate parser object to process given `obj`.

        :param obj:
            a file path, file or file-like object, pathlib.Path object or
            `~anyconfig.globals.IOInfo` (namedtuple) object
        :param forced_type: Forced parser type

        :return: Parser object
        :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
        """
        if obj and not isinstance(obj, anyconfig.globals.IOInfo):
            obj = anyconfig.ioinfo.make(obj)

        psr = super(Parsers, self).find(obj, forced_type=forced_type,
                                        cls=anyconfig.backend.base.Parser)

        LOGGER.debug("Using parser %r [%s]", psr, psr.type())
        return psr

    def list_types(self):
        """List available types parsers support.
        """
        return sorted(set(psr.type() for psr in self.list()))

# vim:sw=4:ts=4:et:
