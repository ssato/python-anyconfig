#
# Copyright (C) 2012 - 2019 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
from __future__ import absolute_import

import tests.backend.common as TBC
from anyconfig.compat import OrderedDict


CNF_S = TBC.read_from_res("20-00-cnf.yml")
CNF = OrderedDict((("a", 0), ("b", "bbb"), ("c", [1, 2, 3]),
                   ("sect0", OrderedDict((("d", "x y z".split()), ))),
                   ("sect1", OrderedDict((("d", "x y z".split()),
                                          ("e", True))))))

# vim:sw=4:ts=4:et:
