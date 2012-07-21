#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato@redhat.com>
#
import copy

# TODO: Keep items' order:
#from collections import OrderedDict as dict


_STRATEGIES = (ST_REPLACE, ST_MERGE_DICTS, ST_MERGE_DICTS_AND_LISTS) = \
(1, 2, 3)


def is_Bunch_or_dict(x):
    return isinstance(x, (Bunch, dict))


def is_iterable(x):
    return isinstance(x, (list, tuple)) or getattr(x, "next", False)


class Bunch(dict):
    """
    Simple class implements 'Bunch Pattern'.

    @see http://ruslanspivak.com/2011/06/12/the-bunch-pattern/
    """

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __getstate__ = dict.copy

    def __setstate__(self, dic):
        self.__dict__ = dic

    def __str__(self):
        """
        Remove special methods and attributes which starts with "__" from
        string representation.
        """
        return str(
            dict((k, v) for k, v in self.iteritems() if not k.startswith("__"))
        )

    def update(self, other, strategy=ST_MERGE_DICTS):
        """Update members recursively based on given strategy.
        """
        if strategy == ST_REPLACE:
            self.update_w_replace(other)
        elif strategy == ST_MERGE_DICTS:
            self.update_w_merge(other)
        elif strategy == ST_MERGE_DICTS_AND_LISTS:
            self.update_w_merge(other, merge_lists=True)
        else:
            self.update_w_merge(other)  # FIXME: Which is suitable for default?

    def update_w_replace(self, other):
        if is_Bunch_or_dict(other):
            for k, v in other.iteritems():
                self[k] = v
        else:
            self = copy.copy(other)

    def update_w_merge(self, other, merge_lists=False):
        """Merge members recursively.

        @param merge_lists: Merge not only dicts but also lists,
            e.g. [1, 2], [3, 4] ==> [1, 2, 3, 4]
        """
        if is_Bunch_or_dict(other):
            for k, v in other.iteritems():
                if k in self and is_Bunch_or_dict(v) and \
                        is_Bunch_or_dict(self[k]):  # update recursively.
                    self[k].update_w_merge(v, merge_lists)
                else:
                    if merge_lists and is_iterable(v):
                        self[k] = self[k] + list(v)
                    else:
                        self[k] = v


# vim:sw=4:ts=4:et:
