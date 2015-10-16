#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""Common options for some public APIs.

.. versionadded:: 0.3
   New module to consolidate some common option processing code exported from
   anyconfig.api.
"""
from __future__ import absolute_import

import anyconfig.mergeabledict


class CommonOptions(dict):
    """Common opitons for loading and dumping functions in anyconfig.api.

    - ac_forced_type: Forced type of configuration parser to load and/or dump
    - ac_parser: Forced configuration parser to load and/or dump
    """

    forced_type = ac_forced_type = None
    ac_parser = None


class SingleLoadOptions(CommonOptions):
    """Opitons for anyconfig.api.single_load.

    - ignore_missing:
        Ignore and just return empty result if given file does not exist
    - ac_template:
        Assume configuration file may be a template file and try to compile it
        AAR if True
    - ac_context: A dict presents context to instantiate template
    - ac_schema: JSON schema file path to validate given config file
    """

    ignore_missing = ac_ignore_missing = False
    ac_template = False
    ac_context = None
    ac_schema = None


class MultiLoadOptions(CommonOptions):
    """Opitons for anyconfig.api.multi_load.

    - merge:
        Strategy to merge config results of multiple config files loaded.
        See also: anyconfig.mergeabledict.MergeableDict.update().
    - marker: Globbing markerer to detect paths patterns
    """
    merge = ac_merge = anyconfig.mergeabledict.MS_DICTS
    marker = ac_merker = '*'

# vim:sw=4:ts=4:et:
