#
# Copyright (C) 2011 - 2018 Satoru SATOH <ssato @ redhat.com>
# Copyright (C) 2019 - 2020 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# Suppress: import positions after some globals are defined
# pylint: disable=wrong-import-position
"""A module to aggregate config parser (loader/dumper) backends.
"""
from __future__ import absolute_import

import warnings

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
import anyconfig.backend.yaml
import anyconfig.backend.xml


PARSERS = [anyconfig.backend.ini.Parser,
           anyconfig.backend.pickle.Parser,
           anyconfig.backend.properties.Parser,
           anyconfig.backend.shellvars.Parser, anyconfig.backend.xml.Parser]

PARSERS.extend(anyconfig.backend.json.PARSERS)

_NA_MSG = "'{}' module is not available. Disabled {} support."

if anyconfig.backend.yaml.PARSERS:
    PARSERS.extend(anyconfig.backend.yaml.PARSERS)
else:
    warnings.warn(_NA_MSG.format("yaml", "YAML"), ImportWarning)

try:
    import anyconfig.backend.toml
    PARSERS.append(anyconfig.backend.toml.Parser)
except ImportError:
    warnings.warn(_NA_MSG.format("toml", "TOML"), ImportWarning)


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

        super().__init__(processors)

# vim:sw=4:ts=4:et:
