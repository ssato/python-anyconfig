#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# Suppress import positions after some global variables are defined
# pylint: disable=wrong-import-position
"""A collection of backend modules available by default."""
import warnings

from . import (
    ini,
    json,
    pickle,
    properties,
    shellvars,
    yaml,
    xml
)
from .base import (
    ParserT, ParsersT, ParserClssT
)


PARSERS: ParserClssT = [
    ini.Parser, pickle.Parser, properties.Parser, shellvars.Parser, xml.Parser
] + json.PARSERS


def warn(name: str, feature: str):
    """An wraper for warnings.warn."""
    warnings.warn(
        f"'{name}' module is not available. Disabled {feature} support.",
        category=ImportWarning, stacklevel=2
    )


if yaml.PARSERS:
    PARSERS.extend(yaml.PARSERS)
else:
    warn('yaml', 'YAML')

try:
    from . import toml
    PARSERS.append(toml.Parser)
except ImportError:
    warn('toml', 'TOML')


__all__ = [
    'ParserT', 'ParsersT', 'ParserClssT',
    'PARSERS',
]

# vim:sw=4:ts=4:et:
