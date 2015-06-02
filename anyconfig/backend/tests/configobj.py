#
# Copyright (C) 2013 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import anyconfig.backend.configobj as TT
import os
import tempfile
import unittest


CONF_0 = """\
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


class Test(unittest.TestCase):

    def setUp(self):
        (_, conf) = tempfile.mkstemp(prefix="ac-bc-test-")
        open(conf, 'w').write(CONF_0)
        self.config_path = conf

    def tearDown(self):
        os.remove(self.config_path)

    def test_00_supports(self):
        self.assertFalse(TT.Parser.supports("/a/b/c/d.json"))

    def test_10_loads(self):
        conf = TT.Parser.loads(CONF_0)

        self.assertEquals(conf['keyword1'], 'value1')
        self.assertEquals(conf['keyword 2'], 'value 2')
        self.assertEquals(conf['section 1']['keyword 3'], 'value 3')
        self.assertEquals(conf['section 1']['keyword 4'],
                          ['value4', 'value 5', 'value 6'])
        self.assertEquals(conf['section 1']['sub-section']['keyword 5'],
                          'value 7')
        self.assertEquals(conf['section 1']['sub-section']['keyword 6'],
                          """A multiline value,
that spans more than one line :-)
The line breaks are included in the value.""")
        self.assertEquals(
            conf['section 1']['sub-section']['sub-sub-section']['keyword 7'],
            'value 8'
        )
        self.assertEquals(conf['section 2']['keyword8'], 'value 9')
        self.assertEquals(conf['section 2']['keyword9'], 'value10')

    def test_20_load(self):
        conf = TT.Parser.load(self.config_path)

        self.assertEquals(conf['keyword1'], 'value1')
        self.assertEquals(conf['keyword 2'], 'value 2')
        self.assertEquals(conf['section 1']['keyword 3'], 'value 3')
        self.assertEquals(conf['section 1']['keyword 4'],
                          ['value4', 'value 5', 'value 6'])
        self.assertEquals(conf['section 1']['sub-section']['keyword 5'],
                          'value 7')
        self.assertEquals(conf['section 1']['sub-section']['keyword 6'],
                          """A multiline value,
that spans more than one line :-)
The line breaks are included in the value.""")
        self.assertEquals(
            conf['section 1']['sub-section']['sub-sub-section']['keyword 7'],
            'value 8'
        )
        self.assertEquals(conf['section 2']['keyword8'], 'value 9')
        self.assertEquals(conf['section 2']['keyword9'], 'value10')

    def test_30_dumps(self):
        conf = TT.Parser.loads(CONF_0)
        conf_s = TT.Parser.dumps(conf)
        conf = TT.Parser.loads(conf_s)

        self.assertEquals(conf['keyword1'], 'value1')
        self.assertEquals(conf['keyword 2'], 'value 2')
        self.assertEquals(conf['section 1']['keyword 3'], 'value 3')
        self.assertEquals(conf['section 1']['keyword 4'],
                          ['value4', 'value 5', 'value 6'])
        self.assertEquals(conf['section 1']['sub-section']['keyword 5'],
                          'value 7')
        self.assertEquals(conf['section 1']['sub-section']['keyword 6'],
                          """A multiline value,
that spans more than one line :-)
The line breaks are included in the value.""")
        self.assertEquals(
            conf['section 1']['sub-section']['sub-sub-section']['keyword 7'],
            'value 8'
        )
        self.assertEquals(conf['section 2']['keyword8'], 'value 9')
        self.assertEquals(conf['section 2']['keyword9'], 'value10')

    def test_40_dump(self):
        conf = TT.Parser.loads(CONF_0)
        TT.Parser.dump(conf, self.config_path)
        conf = TT.Parser.load(self.config_path)

        self.assertEquals(conf['keyword1'], 'value1')
        self.assertEquals(conf['keyword 2'], 'value 2')
        self.assertEquals(conf['section 1']['keyword 3'], 'value 3')
        self.assertEquals(conf['section 1']['keyword 4'],
                          ['value4', 'value 5', 'value 6'])
        self.assertEquals(conf['section 1']['sub-section']['keyword 5'],
                          'value 7')
        self.assertEquals(conf['section 1']['sub-section']['keyword 6'],
                          """A multiline value,
that spans more than one line :-)
The line breaks are included in the value.""")
        self.assertEquals(
            conf['section 1']['sub-section']['sub-sub-section']['keyword 7'],
            'value 8'
        )
        self.assertEquals(conf['section 2']['keyword8'], 'value 9')
        self.assertEquals(conf['section 2']['keyword9'], 'value10')

# vim:sw=4:ts=4:et:
