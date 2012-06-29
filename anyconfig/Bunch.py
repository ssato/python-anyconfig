#
# Copyright (C) 2011, 2012 Satoru SATOH <ssato@redhat.com>
#

# TODO: Keep items' order:
#from collections import OrderedDict as dict


def is_Bunch_or_dict(x):
    return isinstance(x, (Bunch, dict))


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

    def update(self, other):
        """
        Update members recursively.
        """
        if is_Bunch_or_dict(other):
            for k, v in other.iteritems():
                if k in self and is_Bunch_or_dict(v) and \
                        is_Bunch_or_dict(self[k]):
                    self[k].update(v)  # update recursively.
                else:
                    self[k] = v


# vim:sw=4:ts=4:et:
