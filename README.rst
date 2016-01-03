================
python-m9dicts
================

.. .. image:: https://img.shields.io/pypi/v/m9dicts.svg
   :target: https://pypi.python.org/pypi/m9dicts/
   :alt: [Latest Version]

.. .. image:: https://img.shields.io/pypi/pyversions/m9dicts.svg
   :target: https://pypi.python.org/pypi/m9dicts/
   :alt: [Python versions]

.. image:: https://img.shields.io/travis/ssato/python-m9dicts.svg
   :target: https://travis-ci.org/ssato/python-m9dicts
   :alt: [Test status]

.. image:: https://img.shields.io/coveralls/ssato/python-m9dicts.svg
   :target: https://coveralls.io/r/ssato/python-m9dicts
   :alt: [Coverage Status]

.. image:: https://landscape.io/github/ssato/python-m9dicts/master/landscape.png
   :target: https://landscape.io/github/ssato/python-m9dicts/master
   :alt: [Code Health]

.. .. image:: https://scrutinizer-ci.com/g/ssato/python-m9dicts/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/ssato/python-m9dicts
   :alt: [Code Quality]

Overview
=========

python-m9dicts (merge-able dicts) is a `MIT licensed
<http://opensource.org/licenses/MIT>`_ python library provides some dict-like
classes (m9dicts) support recursive merge operations according to each merge
strategy, and some related utility functions (APIs).

- Author: Satoru SATOH <ssato@redhat.com>
- License: MIT
- Home: https://github.com/ssato/python-m9dicts

.. - PyPI: https://pypi.python.org/pypi/m9dicts

Usage
-------

APIs
^^^^^^

m9dicts.make is a factory function to make m9dicts supports recursive merge operation.

Here are some examples of m9dicts.make usages:

::

    >>> import m9dicts
    >>> mzero = m9dicts.make()  # It just makes an empty m9dict object.
    >>> m9d0 = m9dicts.make(dict(a=1, b=2, c=3))   # Make from a dict.
    >>> m9d1 = m9dicts.make(OrderedDict((("a", 1), ("b", 2)))   # Make from an OrderedDict.

Default m9dict class is m9dicts.UpdateWithMergeDict and it's selectable by the
keyword arguments 'ordered' and 'merge': 

- ordered: Set True if you want to keep the order of keys of made m9dict object
- merge: Pass one of:

  - m9dicts.MS_DICTS: It's the default. m9dicts.UpdateWithMergeDict or m9dicts.UpdateWithMergeOrderedDict (if ordered == True) will be chosen.
  - m9dicts.MS_DICTS_AND_LISTS: Like the above but lists are also merged and m9dicts.UpdateWithMergeListsDict or UpdateWithMergeListsOrderedDict will be chosen.
  - m9dicts.MS_NO_REPLACE: m9dicts.UpdateWoReplaceDict or m9dicts.UpdateWoReplaceOrderedDict will be chosen.
  - m9dicts.MS_REPLACE: m9dicts.UpdateWithReplaceDict or m9dicts.UpdateWithReplaceOrderedDict will be chosen.

Please take a look at the next section for more details of each m9dict classes.

m9dicts.get is to get value from nested dicts of which key is given by some
path expressions. For example,

::

    >>> d = {'a': {'b': {'c': 0, 'd': [1, 2]}}, '': 3}
    >>> get(d, '/')  # key becomes '' (empty string).
    (3, '')
    >>> get(d, "/a/b/c")
    (0, '')
    >>> sorted(get(d, "a.b")[0].items())
    [('c', 0), ('d', [1, 2])]
    >>> (get(d, "a.b.d"), get(d, "/a/b/d/1"))
    (([1, 2], ''), (2, ''))
    >>> get(d, "a.b.key_not_exist")  # doctest: +ELLIPSIS
    (None, "'...'")
    >>> get(d, "/a/b/d/2")
    (None, 'list index out of range')
    >>> get(d, "/a/b/d/-")  # doctest: +ELLIPSIS
    (None, 'list indices must be integers...')

Supported path expressions are followings.

- Javascript object notation like (join keys with '.')
- File path like (join keys with '/')
- JSON Pointer [#]_ expression

m9dicts.set\_ is to set value to nested dicts of which key is given by some
path expressions like followings.

- Javascript object notation like (join keys with '.')
- File path like (join keys with '/')

m9dicts.convert_to is an utility function to convert m9dicts to a dict or namedtuple object recursively.

.. [#] http://tools.ietf.org/html/rfc6901

Dict types
^^^^^^^^^^^^

m9dicts provides some m9dict (merge-able dict) classes merging (maybe nested)
dicts recursively according to different merge strategy.

.. csv-table::
   :header: "m9dict class", "Keep keys order?", strategy
   :widths: 15, 20, 30

   UpdateWithReplaceDict, No, Replace value of dict to update with other's if both have same keys on update.
   UpdateWithReplaceOrderedDict, Yes, Likewise but the order of keys are kept.
   UpdateWoReplaceDict, No, "Never update (replace) the value of dict ot update with other's, that is, only the values it does not have the key will be added on update." 
   UpdateWoReplaceOrderedDict, Yes, Likewise but the order of keys are kept.
   UpdateWithMergeDict, No, Merge the value of dict to update with other's recursively. Behavior of merge will be vary depends on types of original and new values.
   UpdateWithMergeOrderedDict, Yes, Likewise but the order of keys are kept.
   UpdateWithMergeListsDict, No, Merge recursively like UpdateWithMergeDict but lists will be concatenated.
   UpdateWithMergeListsOrderedDict, Yes, Likewise but the order of keys are kept.

See also each m9dict class in m9dicts.dicts.

Installation
==============

Requirements
-------------

python-m9dicts just works with python standard library except that ordereddict
is required for python 2.6 envrionment.

.. csv-table::
   :header: Requirement, URL, Notes
   :widths: 15, 25, 30

   ordereddict, https://pypi.python.org/pypi/ordereddict/, required only for python 2.6 env.

How to Install
----------------

- pip:

  .. code-block:: console
     
     $ pip install git+https://github.com/ssato/python-m9dicts/

- make rpm and install it:

  - build srpm and then rpm with using mock:

  .. code-block:: console

     $ python setup.py srpm
     $ mock dist/python-m9dicts-<ver_dist...>.src.rpm
     $ sudo yum install -y /var/lib/mock/<build_dist>/results/python-m9dicts-<ver_dist...>.noarch.rpm

  - build rpm:

  .. code-block:: console

     $ python setup.py rpm
     $ sudo yum install -y dist/\*.noarch.rpm

Hacking
========

Help and feedback
-------------------

If you have any issues / feature request / bug reports with python-m9dicts,
please open an issue ticket on github.com
(https://github.com/ssato/python-m9dicts/issues).

Test
------

Run '[WITH_COVERAGE=1] ./pkg/runtest.sh [path_to_python_code]' or 'tox' for tests.
For example,

.. code-block:: console

   $ WITH_COVERAGE=1 ./pkg/runtest.sh 2>&1 | tee /tmp/t.log

About test-time requirements, please take a look at pkg/test_requirements.txt.

.. Customization
.. ---------------


.. vim:sw=4:ts=4:et:
