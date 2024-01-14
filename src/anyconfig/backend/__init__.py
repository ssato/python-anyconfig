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
    python,
    sh,
    toml,
    yaml,
    xml
)
from .base import (
    ParserT, ParsersT, ParserClssT
)


PARSERS: ParserClssT = [
    *ini.PARSERS, *json.PARSERS, *pickle.PARSERS, *properties.PARSERS,
    *python.PARSERS, *sh.PARSERS, *xml.PARSERS,
]


def warn(name: str, feature: str):
    """Wraper for warnings.warn."""
    warnings.warn(
        f"'{name}' module is not available. Disabled {feature} support.",
        category=ImportWarning, stacklevel=2
    )


if yaml.PARSERS:
    PARSERS.extend(yaml.PARSERS)
else:
    warn('yaml', 'YAML')

if toml.PARSERS:
    PARSERS.extend(toml.PARSERS)
else:
    warn('toml', 'TOML')


__all__ = [
    'ParserT', 'ParsersT', 'ParserClssT',
    'PARSERS',
]

# vim:sw=4:ts=4:et:
