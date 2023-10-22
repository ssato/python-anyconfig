#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=raise-missing-from
from collections import OrderedDict as ODict


CNF = ODict((('title', 'TOML Example'),
             ('owner',
              ODict((('name', 'Tom Preston-Werner'),
                     ('dob', '1979-05-27T07:32:00Z')))),
             ('database',
              ODict((('server', '192.168.1.1'),
                     ('ports', [8001, 8001, 8002]),
                     ('connection_max', 5000),
                     ('enabled', True)))),
             ('servers',
              ODict((('alpha',
                      ODict((('ip', '10.0.0.1'), ('dc', 'eqdc10')))),
                     ('beta',
                      ODict((('ip', '10.0.0.2'), ('dc', 'eqdc10'))))))),
             ('clients',
              ODict((('data', [['gamma', 'delta'], [1, 2]]),
                     ('hosts', ['alpha', 'omega']))))))
