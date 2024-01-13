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
And anyconfig.backend.tests.ini.Test10 and anyconfig.backend.tests.ini.Test20
may help to write test cases of these methods.

JSON and YAML backend modules (anyconfig.backend.{json,yaml}_) should be good
examples to write backend modules and its test cases, I think.

Also, please take a look at some example backend plugin modules mentioned in
the Supported configuration formats section.

How to test backend modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Basically, you only need to do the followings to test loaders.

- Arrange test data (input file, expected output and option file) under tests/res/1/loaders/<parser's cid>/[0-9]{2}/

  - Arange input file of the file type parser expects as inputs:

    - example #1. tests/res/1/loaders/json.stdlib/10/360_a_nested_map.json (json)
    - example #2. tests/res/1/loaders/sh.variables/10/100_basics.sh

  - Arange expected output files as python code (.py) or json (.json) data with name, <input_filename>.<extension>

    - example #1. tests/res/1/loaders/json.stdlib/10/e/360_a_nested_map.json.py
    - example #2. tests/res/1/loaders/sh.variables/10/e/100_basics.sh.json

  - Optionaly, arrange data file contains options given to paser.load{,s} functions

    - tests/res/1/loaders/json.stdlib/20/o/360_a_nested_map.json.json

- Arrange test code as tests/backend/loader/<ype>/<laoder_filename> by either way of the followings

  - Make a symlink to tests/backend/loaders/json/test_json_stdlib.py if any modifications are not needed

    - example: tests/backend/loaders/xml/test_xml_etree.py

  - Copy tests/backend/loaders/json/test_json_stdlib.py and modify as you need

    - example: tests/backend/loaders/toml/test_toml_tomllib.py

See also the actual examples under tests/backend/ and tests/res/1/loaders/

And for dumers, do same thing as doing for loaders.

.. vim:sw=2:ts=2:et:
