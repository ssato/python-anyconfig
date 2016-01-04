#
# Copyright (C) 2011 - 2015 Red Hat, Inc.
# Copyright (C) 2011 - 2016 Satoru SATOH <ssato redhat.com>
# License: MIT
#
# .. note:: suppress warning about import error of ordereddict only for py-2.6.
# pylint: disable=import-error
"""Some dict-like classes support merge operations.
"""
from __future__ import absolute_import


# Merge strategies:
MS_REPLACE = "replace"
MS_NO_REPLACE = "noreplace"
MS_DICTS = "merge_dicts"
MS_DICTS_AND_LISTS = "merge_dicts_and_lists"
MERGE_STRATEGIES = (MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS)

# vim:sw=4:ts=4:et:
