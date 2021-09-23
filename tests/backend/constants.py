#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
import copy

from collections import OrderedDict


CNF_0 = OrderedDict((('DEFAULT', OrderedDict((('a', '0'), ('b', 'bbb'),
                                              ('c', '5')))),
                     ('sect0', OrderedDict((('a', '0'), ('b', 'bbb'),
                                            ('c', '5'),
                                            ('d', 'x,y,z'))))))
CNF_1 = copy.deepcopy(CNF_0)
CNF_1['sect0']['d'] = CNF_1['sect0']['d'].split()

CNF_2 = OrderedDict((('a', 0.1),
                     ('b', b'bbb'),
                     ('sect0',
                      OrderedDict((('c', [b'x', b'y', b'z']), )))))

# vim:sw=4:ts=4:et:
