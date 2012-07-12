#
# Copyright (C) 2011, 2012 Satoru SATOH <satoru.satoh @ gmail.com>
#
import anyconfig.Bunch as B
import anyconfig.tests.common as C

import cPickle as pickle
import os.path
import unittest


class TestBunch(unittest.TestCase):

    def test_create_set_and_get(self):
        name = "Bunch"
        category = "pattern"
        tags = ["a", "b", "c"]
        newkey = "newkey"

        bunch = B.Bunch(name=name, category=category, tags=tags)

        self.assertEquals(bunch.name, name)
        self.assertEquals(bunch.category, category)
        self.assertEquals(bunch.tags, tags)

        self.assertEquals(bunch["name"], name)
        self.assertEquals(bunch["category"], category)
        self.assertEquals(bunch["tags"], tags)

        self.assertFalse(newkey in bunch)

        bunch.newkey = True
        self.assertTrue(newkey in bunch)

        # TODO: The order of keys may be lost currently.
        #self.assertEquals(bunch.keys(), ("name", "category", "newkey"))

    def test_update__w_merge_dicts(self):
        a = B.Bunch(name="a", a=1, b=B.Bunch(b=[1, 2], c="C"))
        b = B.Bunch(a=2, b=B.Bunch(b=[1, 2, 3], d="D"))

        ref = B.Bunch(**a.copy())
        ref.a = 2
        ref.b = B.Bunch(b=[1, 2, 3], c="C", d="D")

        a.update(b)

        self.assertEquals(a, ref)

    def test_update__w_merge_dicts_and_lists(self):
        a = B.Bunch(name="a", a=1, b=B.Bunch(b=[1, 2], c="C"))
        b = B.Bunch(a=2, b=B.Bunch(b=[3, 4, 5], d="D"))

        ref = B.Bunch(**a.copy())
        ref.a = 2
        ref.b = B.Bunch(b=[1, 2, 3, 4, 5], c="C", d="D")

        a.update(b, B.ST_MERGE_DICTS_AND_LISTS)

        self.assertEquals(a, ref)

    def test_update__w_replace(self):
        a = B.Bunch(name="a", a=1, b=B.Bunch(b=[1, 2], c="C"))
        b = B.Bunch(a=2, b=B.Bunch(b=[3, 4, 5], d="D"))

        ref = B.Bunch(**a.copy())
        ref.a = 2
        ref.b = b.b
        ref.b.c = a.b.c

        a.update(b, B.ST_REPLACE)

        self.assertEquals(a, ref)

    def test_update__w_None(self):
        a = B.Bunch(name="a", a=1, b=B.Bunch(b=[1, 2], c="C"))
        ref = B.Bunch(**a.copy())

        a.update(None)

        self.assertEquals(a, ref)


class TestBunch_pickle(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_pickle(self):
        name = "Bunch"
        tags = ["a", "b", "c"]

        bunch = B.Bunch(name=name, tags=tags)

        bf = os.path.join(self.workdir, "test.pkl")
        pickle.dump(bunch, open(bf, "wb"))

        bunch2 = pickle.load(open(bf, "rb"))

        self.assertEquals(bunch2.name, bunch.name)
        self.assertEquals(bunch2.tags, bunch.tags)

        self.assertEquals(bunch2["name"], bunch["name"])
        self.assertEquals(bunch2["tags"], bunch["tags"])

        self.assertEquals(str(bunch2), str(bunch))


# vim:sw=4:ts=4:et:
