#
# Copyright (C) 2013 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""test cases of anyconfig.cli.main with schema options.
"""
from .. import base
from . import collectors, test_base


class Collector(collectors.Collector):
    kind = 'extra_options'


class TestCase(test_base.BaseTestCase):
    collector = Collector()

    def post_checks(self, tdata, *args, **kwargs):
        """Post checks to compare the outputs of ref. and result.

        .. seealso:: tests.cli.test_base.BaseTestCase._run_main
        """
        ref_path = base.maybe_data_path(
            tdata.datadir / 'r', tdata.inp_path.stem
        )
        ref = ref_path.read_text().strip().rstrip()
        out = args[0].read_text().strip().rstrip()
        self.assertEqual(out, ref)

# vim:sw=4:ts=4:et:
