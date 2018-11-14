#
# Copyright (C) 2011 - 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# type() is used to exactly match check instead of isinstance here.
# pylint: disable=unidiomatic-typecheck
r"""YAML backend:

- Format to support: YAML, http://yaml.org
- Requirements:

  - ruamel.yaml, https://bitbucket.org/ruamel/yaml
  - or PyYAML (yaml), http://pyyaml.org

- Development Status :: 5 - Production/Stable
- Limitations:

  - Resuls is not ordered even if 'ac_ordered' or 'ac_dict' was given if PyYAML
    is used as the YAML backend.

- Special options:

  - All keyword options of yaml.safe_load, yaml.load, yaml.safe_dump and
    yaml.dump should work. Also, some keyword options specific for ruamel.yaml
    are supported to enable some its own features PyYAML does not have.

  - Use 'ac_safe' boolean keyword option if you prefer to call yaml.safe_load
    and yaml.safe_dump instead of yaml.load and yaml.dump. Please note that
    this option conflicts with 'ac_dict' option and these options cannot be
    used at the same time.

  - See also: http://pyyaml.org/wiki/PyYAMLDocumentation and
    https://yaml.readthedocs.io/en/latest/

Changelog:

.. versionchanged:: 0.9.8

   - Split PyYaml-based and ruamel.yaml based backend modules
   - Add support of some of ruamel.yaml specific features.

.. versionchanged:: 0.9.3

   - Try ruamel.yaml instead of yaml (PyYAML) if it's available.

.. versionchanged:: 0.3

   - Changed special keyword option 'ac_safe' from 'safe' to avoid
     possibility of option conflicts in the future.
"""
from __future__ import absolute_import
from . import pyyaml


PARSERS = [pyyaml.Parser]

# vim:sw=4:ts=4:et:
