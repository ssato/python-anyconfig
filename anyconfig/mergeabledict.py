#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato@redhat.com>
#
import anyconfig.utils as U
import copy

# TODO: Keep items' order:
#from collections import OrderedDict as dict


(ST_REPLACE, ST_MERGE_DICTS, ST_MERGE_DICTS_AND_LISTS) = (0, 1, 2)


def is_MergeableDict_or_dict(x):
    return isinstance(x, (MergeableDict, dict))


class MergeableDict(dict):
    """
    Dict based object supports 'merge' operation.
    """

    # TODO: Which strategy should be choosen for default?
    strategy = ST_MERGE_DICTS_AND_LISTS

    def get_strategy(self):
        return self.strategy

    def update(self, other, strategy=None):
        """Update members recursively based on given strategy.
        """
        if strategy is None:
            strategy = self.get_strategy()

        if strategy == ST_REPLACE:
            self.update_w_replace(other)
        elif strategy == ST_MERGE_DICTS_AND_LISTS:
            self.update_w_merge(other, merge_lists=True)
        else:
            self.update_w_merge(other, merge_lists=False)

    def update_w_replace(self, other):
        if is_MergeableDict_or_dict(other):
            for k, v in other.iteritems():
                self[k] = v
        else:
            self = copy.copy(other)

    def update_w_merge(self, other, merge_lists=False):
        """Merge members recursively.

        :param merge_lists: Merge not only dicts but also lists. For example,

            [1, 2, 3], [3, 4] ==> [1, 2, 3, 4]
            [1, 2, 2], [2, 4] ==> [1, 2, 2, 4]
        """
        if is_MergeableDict_or_dict(other):
            for k, v in other.iteritems():
                if k in self and is_MergeableDict_or_dict(v) and \
                        is_MergeableDict_or_dict(self[k]):  # update recursively.
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
