#! /bin/bash
set -e

curdir=${0%/*}
topdir=${curdir}/../

which pep8 2>&1 > /dev/null && check_with_pep8=1 || check_with_pep8=0

if test $# -gt 0; then
    test $check_with_pep8 = 1 && (for x in $@; do pep8 ${x%%:*}; done) || :
    PYTHONPATH=$topdir nosetests -c $curdir/nose.cfg $@
else
    test $check_with_pep8 = 1 && (find anyconfig -name '*.py' | xargs pep8) || :
    PYTHONPATH=$topdir nosetests -c $curdir/nose.cfg \
        --with-coverage \
        --cover-tests \
        --cover-inclusive \
        -w $topdir/anyconfig
fi
