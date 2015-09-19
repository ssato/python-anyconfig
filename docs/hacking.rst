Hacking
--------

How to test
^^^^^^^^^^^^^

Run '[WITH_COVERAGE=1] ./pkg/runtest.sh [path_to_python_code]' or 'tox' for tests.

About test-time requirements, please take a look at pkg/test_requirements.txt.

How to write backend plugin modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Backend class must inherit anyconfig.backend.base.Parser or its children in
anyconfig.backend.base module and need some members and methods such as
:meth:`load_from_string`, :meth:`load_from_path`, :meth:`load_from_stream`,
:meth:`dump_to_string`, :meth:`dump_to_path` and :meth:`dump_to_stream`.

JSON and YAML backend modules (anyconfig.backend.{json,yaml}_) should be good
examples to write backend modules, I think.

Also, please take a look at some example backend plugin modules mentioned in
the `Supported configuration formats`_ section.

.. vim:sw=2:ts=2:et:
