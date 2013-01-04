#! /bin/bash
set -e

curdir=${0%/*}
topdir=${curdir}/../

if `env | grep -q 'WITH_COVERAGE' 2>/dev/null`; then
    coverage_opts="--with-coverage --cover-tests --cover-inclusive"
fi

which pep8 2>&1 > /dev/null && check_with_pep8=1 || check_with_pep8=0

if test $# -gt 0; then
    test $check_with_pep8 = 1 && (for x in $@; do pep8 ${x%%:*}; done) || :
    PYTHONPATH=$topdir nosetests -c $curdir/nose.cfg ${coverage_opts} $@
else
    # Find out python package dir and run tests for .py files under it.
    for d in ${topdir}/*; do
        if test -d $d -a -f $d/__init__.py; then
            pypkgdir=$d

            for f in $(find ${pypkgdir} -name '*.py'); do
                echo "[Info] Check $f..."
                test $check_with_pep8 = 1 && pep8 $f || :
                PYTHONPATH=$topdir nosetests -c $curdir/nose.cfg \
                        ${coverage_opts} $f
            done

            break
        fi
    done
fi
