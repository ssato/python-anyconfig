#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, relative-beyond-top-level
from ..multi_load import test_query as multi
from ..single_load import test_query as single
from . import common


class SingleTestCase(common.SingleBase, single.TestCase):
    pass


class MultiTestCase(common.MultiBase, multi.TestCase):
    pass


# vim:sw=4:ts=4:et:
