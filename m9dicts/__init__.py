"""
.. module:: m9dicts
   :synopsis: dict-like objects support recursive merge operations
"""
from .globals import MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS
from .dicts import (
    UpdateWithReplaceDict, UpdateWoReplaceDict, UpdateWithMergeDict,
    UpdateWithMergeListsDict, UpdateWithReplaceOrderedDict,
    UpdateWoReplaceOrderedDict, UpdateWithMergeOrderedDict,
    UpdateWithMergeListsOrderedDict
)
from .api import get, set_, make, convert_to

__author__ = "Satoru SATOH <ssato@redhat.com>"
__version__ = "0.1.0"
# vim:sw=4:ts=4:et:
