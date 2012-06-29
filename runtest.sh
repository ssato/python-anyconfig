#! /bin/bash
set -e


topdir=${0%/*}

which pep8 2>&1 > /dev/null && check_with_pep8=1 || check_with_pep8=0

if test $# -gt 0; then
    test $check_with_pep8 = 1 && (for x in $@; do pep8 ${x%%:*}; done) || :
    PYTHONPATH=$topdir nosetests -c $topdir/nose.cfg $@
else
    PYTHONPATH=$topdir nosetests -c $topdir/nose.cfg -w $topdir/tests/
fi
