#
# Copyright (C) 2011 - 2013 Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""Merge-able dict.
"""
from anyconfig.compat import iteritems

import anyconfig.utils as U
import copy

# TODO: Keep items' order:
# from collections import OrderedDict as dict


MS_REPLACE = "replace"
MS_NO_REPLACE = "noreplace"
MS_DICTS = "merge_dicts"
MS_DICTS_AND_LISTS = "merge_dicts_and_lists"

MERGE_STRATEGIES = (MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS)


def is_mergeabledict_or_dict(obj):
    """
    :param obj: Any object may be an instance of MergeableDict or dict.

    >>> is_mergeabledict_or_dict("a string")
    False
    >>> is_mergeabledict_or_dict({})
    True
    >>> is_mergeabledict_or_dict(create_from({}))
    True
    """
    return isinstance(obj, (MergeableDict, dict))


def convert_to(mdict):
    """
    Convert a MergeableDict instances to a dict object.

    Borrowed basic idea and implementation from bunch.unbunchify.
    (bunch is distributed under MIT license same as this module.)

    :param mdict: A MergeableDict instance
    :return: A dict
    """
    if is_mergeabledict_or_dict(mdict):
        return dict((k, convert_to(v)) for k, v in iteritems(mdict))
    elif U.is_iterable(mdict):
        return type(mdict)(convert_to(v) for v in mdict)
    else:
        return mdict


def create_from(dic):
    """
    Try creating a MergeableDict instance[s] from a dict or any other objects.

    :param dic: A dict instance
    """
    if is_mergeabledict_or_dict(dic):
        return MergeableDict((k, create_from(v)) for k, v in iteritems(dic))
    elif U.is_iterable(dic):
        return type(dic)(create_from(v) for v in dic)
    else:
        return dic


class MergeableDict(dict):
    """
    Dict based object supports 'merge' operation.
    """

    # TODO: Which strategy should be choosen for default?
    strategy = MS_DICTS

    @classmethod
    def create(cls, obj):
        """Create an instance from any object."""
        return create_from(obj)

    @classmethod
    def convert_to(cls, mdict):
        """Create an object from MergeableDict instances"""
        return convert_to(mdict)

    def get_strategy(self):
        """Merge strategy"""
        return self.strategy

    def update(self, other, strategy=None):
        """Update members recursively based on given strategy.

        :param other: Other MergeableDict instance to merge
        :param strategy: Merge strategy
        """
        if strategy is None:
            strategy = self.get_strategy()

        if strategy == MS_REPLACE:
            self.update_w_replace(other)
        elif strategy == MS_NO_REPLACE:
            self.update_wo_replace(other)
        elif strategy == MS_DICTS_AND_LISTS:
            self.update_w_merge(other, merge_lists=True)
        else:
            self.update_w_merge(other, merge_lists=False)

    def update_w_replace(self, other):
        """Update and replace self w/ other if both has same keys.

        :param other: object of which type is same as self's.

        >>> md0 = MergeableDict.create(dict(a=1, b=[1, 3], c="abc"))
        >>> md1 = MergeableDict.create(dict(a=2, b=[0, 1], c="xyz"))
        >>> md0.update_w_replace(md1)
        >>> all(md0[k] == md1[k] for k in ("a", "b", "c"))
        True
        """
        if is_mergeabledict_or_dict(other):
            for k, v in iteritems(other):
                self[k] = v
        else:
            self = copy.copy(other)

    def update_wo_replace(self, other):
        """Update self w/ other but never replace self w/ other.

        >>> md0 = md1 = MergeableDict.create(dict(a=1, b=[1, 3], c="abc"))
        >>> md2 = MergeableDict.create(dict(a=2, b=[0, 1], c="xyz", d=None))
        >>> md0.update_wo_replace(md2)
        >>> all(md0[k] != md2[k] for k in ("a", "b", "c"))
        True
        >>> all(md0[k] == md1[k] for k in ("a", "b", "c"))
        True
        >>> md0["d"] == md2["d"]
        True
        """
        if is_mergeabledict_or_dict(other):
            for k, v in iteritems(other):
                if k not in self:
                    self[k] = v

    def update_w_merge(self, other, merge_lists=False):
        """Merge members recursively.

        :param merge_lists: Merge not only dicts but also lists. For example,

            [1, 2, 3], [3, 4] ==> [1, 2, 3, 4]
            [1, 2, 2], [2, 4] ==> [1, 2, 2, 4]

        >>> md0 = md1 = MergeableDict.create(dict(a=1, b=dict(c=2, d=3),
        ...                                       e=[1, 2]))
        >>> md2 = MergeableDict.create(dict(a=2, b=dict(d=4, f=5), e=[3, 4]))
        >>> md0.update_w_merge(md2, False)
        >>> md0["a"] == md2["a"]
        True
        >>> md0["b"]["d"] == md2["b"]["d"] and md0["b"]["f"] == md2["b"]["f"]
        True
        >>> md0["e"] == md2["e"]
        True

        # TODO:
        # >>> md1.update_w_merge(md2, True)
        # >>> md0["e"] == [1, 2, 3, 4]
        # True
        """
        if is_mergeabledict_or_dict(other):
            for k, v in iteritems(other):
                if k in self and is_mergeabledict_or_dict(v) and \
                        is_mergeabledict_or_dict(self[k]):
                    # update recursively.
                    self[k].update_w_merge(v, merge_lists)
                else:
                    if merge_lists and U.is_iterable(v):
                        v0 = self.get(k, None)
                        if v0 is None:
                            self[k] = [x for x in list(v)]
                        else:
                            self[k] += [x for x in list(v) if x not in v0]
                    else:
                        self[k] = v

# vim:sw=4:ts=4:et:
