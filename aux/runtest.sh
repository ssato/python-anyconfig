#! /bin/bash
set -e

curdir=${0%/*}
topdir=${curdir}/../

#coverage_opts="--with-coverage --cover-tests --cover-inclusive"
coverage_opts=""

which pep8 2>&1 > /dev/null && check_with_pep8=1 || check_with_pep8=0

if test $# -gt 0; then
    test $check_with_pep8 = 1 && (for x in $@; do pep8 ${x%%:*}; done) || :
    PYTHONPATH=$topdir nosetests -c $curdir/nose.cfg $@
else
    for f in $(find ${topdir}/anyconfig -name '*.py'); do
        echo "[Info] Check $f..."
        test $check_with_pep8 = 1 && pep8 $f || :
        PYTHONPATH=$topdir nosetests -c $curdir/nose.cfg ${coverage_opts} $f
    done
fi
