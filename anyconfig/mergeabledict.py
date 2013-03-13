#
# Copyright (C) 2011 - 2013 Satoru SATOH <ssato redhat.com>
# License: MIT
#
import anyconfig.utils as U
import copy

# TODO: Keep items' order:
#from collections import OrderedDict as dict


MS_REPLACE = "replace"
MS_NO_REPLACE = "noreplace"
MS_DICTS = "merge_dicts"
MS_DICTS_AND_LISTS = "merge_dicts_and_lists"

MERGE_STRATEGIES = (MS_REPLACE, MS_NO_REPLACE, MS_DICTS, MS_DICTS_AND_LISTS)


def is_MergeableDict_or_dict(x):
    return isinstance(x, (MergeableDict, dict))


def convert_to(x):
    """
    Convert a MergeableDict instances to a dict object.

    Borrowed basic idea and implementation from bunch.unbunchify.
    (bunch is distributed under MIT license same as this module.)
    """
    if is_MergeableDict_or_dict(x):
        return dict((k, convert_to(v)) for k, v in x.iteritems())
    elif U.is_iterable(x):
        return type(x)(convert_to(v) for v in x)
    else:
        return x


def create_from(x):
    """
    Try creating a MergeableDict instance[s] from a dict or any other objects.
    """
    if is_MergeableDict_or_dict(x):
        return MergeableDict((k, create_from(v)) for k, v in x.iteritems())
    elif U.is_iterable(x):
        return type(x)(create_from(v) for v in x)
    else:
        return x


class MergeableDict(dict):
    """
    Dict based object supports 'merge' operation.
    """

    # TODO: Which strategy should be choosen for default?
    strategy = MS_DICTS

    @classmethod
    def create(cls, x):
        """Create an instance from any object."""
        return create_from(x)

    @classmethod
    def convert_to(cls, x):
        return convert_to(x)

    def get_strategy(self):
        return self.strategy

    def update(self, other, strategy=None):
        """Update members recursively based on given strategy.
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
        """
        if is_MergeableDict_or_dict(other):
            for k, v in other.iteritems():
                self[k] = v
        else:
            self = copy.copy(other)

    def update_wo_replace(self, other):
        """Update self w/ other but never replace self w/ other.
        """
        if is_MergeableDict_or_dict(other):
            for k, v in other.iteritems():
                if k not in self:
                    self[k] = v

    def update_w_merge(self, other, merge_lists=False):
        """Merge members recursively.

        :param merge_lists: Merge not only dicts but also lists. For example,

            [1, 2, 3], [3, 4] ==> [1, 2, 3, 4]
            [1, 2, 2], [2, 4] ==> [1, 2, 2, 4]
        """
        if is_MergeableDict_or_dict(other):
            for k, v in other.iteritems():
                if k in self and is_MergeableDict_or_dict(v) and \
                        is_MergeableDict_or_dict(self[k]):
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
