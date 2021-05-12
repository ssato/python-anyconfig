#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# Suppress import positions after some global variables are defined
# pylint: disable=wrong-import-position
"""A collection of default backend modules.
"""
import typing
import warnings

from . import (
    base,
    ini,
    json,
    pickle,
    properties,
    shellvars,
    yaml,
    xml
)


ParserT = typing.TypeVar('ParserT', bound=base.Parser)
ParsersT = typing.List[ParserT]

PARSERS: ParsersT = [
    ini.Parser, pickle.Parser, properties.Parser, shellvars.Parser, xml.Parser
] + json.PARSERS

_NA_MSG = "'{}' module is not available. Disabled {} support."

if yaml.PARSERS:
    PARSERS.extend(yaml.PARSERS)
else:
    warnings.warn(_NA_MSG.format('yaml', 'YAML'), ImportWarning)

try:
    from . import toml
    PARSERS.append(toml.Parser)
except ImportError:
    warnings.warn(_NA_MSG.format('toml', 'TOML'), ImportWarning)

# vim:sw=4:ts=4:et:
