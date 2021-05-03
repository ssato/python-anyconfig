#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""YAML backends:

- pyyaml: PyYAML, http://pyyaml.org [default]
- ruamel.yaml: ruamel.yaml, https://bitbucket.org/ruamel/yaml

Changelog:

.. versionchanged:: 0.9.8

   - Split PyYaml-based and ruamel.yaml based backend modules
   - Add support of some of ruamel.yaml specific features.
"""
import typing

import anyconfig.backend.base


ParserTVar = typing.TypeVar('ParserTVar', bound=anyconfig.backend.base.Parser)
try:
    from . import pyyaml
    PARSERS: typing.List[ParserTVar] = [pyyaml.Parser]
except ImportError:
    PARSERS: typing.List[ParserTVar] = []

try:
    from . import ruamel_yaml as ryaml
    PARSERS.append(ryaml.Parser)
except ImportError:
    ryaml = False

# vim:sw=4:ts=4:et:
