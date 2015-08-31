#
# Copyright (C) 2013 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os
import tempfile
import unittest

import anyconfig.backend.configobj as TT
from anyconfig.tests.common import dicts_equal


CNF_0_S = """\
# This is the 'initial_comment'
# Which may be several lines
keyword1 = value1
'keyword 2' = 'value 2'

[ "section 1" ]
# This comment goes with keyword 3
keyword 3 = value 3
'keyword 4' = value4, value 5, 'value 6'

    [[ sub-section ]]    # an inline comment
    # sub-section is inside "section 1"
    'keyword 5' = 'value 7'
    'keyword 6' = '''A multiline value,
that spans more than one line :-)
The line breaks are included in the value.'''

        [[[ sub-sub-section ]]]
        # sub-sub-section is *in* 'sub-section'
        # which is in 'section 1'
        'keyword 7' = 'value 8'

[section 2]    # an inline comment
keyword8 = "value 9"
keyword9 = value10     # an inline comment
# The 'final_comment'
# Which also may be several lines
"""

_ML_0 = """A multiline value,
that spans more than one line :-)
The line breaks are included in the value."""

CNF_0 = {'keyword 2': 'value 2',
         'keyword1': 'value1',
         'section 1': {'keyword 3': 'value 3',
                       'keyword 4': ['value4', 'value 5', 'value 6'],
                       'sub-section': {'keyword 5': 'value 7',
                                       'keyword 6': _ML_0,
                                       'sub-sub-section': {
                                           'keyword 7': 'value 8'}}},
         'section 2': {'keyword8': 'value 9', 'keyword9': 'value10'}}


class Test10(unittest.TestCase):

    cnf = CNF_0
    cnf_s = CNF_0_S

    def test_10_loads(self):
        cnf = TT.Parser().loads(self.cnf_s)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_30_dumps(self):
        cnf_s = TT.Parser().dumps(self.cnf)
        cnf = TT.Parser().loads(cnf_s)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))


class Test20(unittest.TestCase):

    cnf = CNF_0
    cnf_s = CNF_0_S

    def setUp(self):
        (_, self.cpath) = tempfile.mkstemp(prefix="ac-bc-test-")
        open(self.cpath, 'w').write(self.cnf_s)

    def tearDown(self):
        os.remove(self.cpath)

    def test_20_load(self):
        cnf = TT.Parser().load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_40_dump(self):
        TT.Parser().dump(self.cnf, self.cpath)  # Overwrite it.
        cnf = TT.Parser().load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
