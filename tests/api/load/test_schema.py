#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, relative-beyond-top-level
from ..multi_load import test_schema as multi
from . import common


class MultiTestCase(common.MultiBase, multi.TestCase):
    pass
