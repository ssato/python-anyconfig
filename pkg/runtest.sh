#! /bin/bash
set -e

curdir=${0%/*}
topdir=${curdir}/../
nosetests_opts="-c ${curdir}/nose.cfg"
nprocs=$(echo ${NOSE_PROCESSES})

if `env | grep -q 'WITH_COVERAGE' 2>/dev/null`; then
    nosetests_opts="${nosetests_opts} --with-coverage --cover-tests"
    nprocs=0  # It seems that coverage does not like parallel tests.
fi

if test "x${nprocs}" != "x0" ; then
    if test -f /proc/cpuinfo; then
        nprocs=$(sed -n '/^processor.*/p' /proc/cpuinfo | wc -l)
        if test ${nprocs} -gt 0; then
            nosetests_opts="${nosetests_opts} --processes=${nprocs}"
        fi
    fi
fi

if `which pep8 2>&1 > /dev/null`; then
    #pep8_opts="--statistics --benchmark"
    if `which flake8 2>&1 > /dev/null`; then
        pep8_opts="$pep8_opts --doctests"
        function _pep8 () { flake8 $pep8_opts $@; }
    else
        function _pep8 () { pep8 $pep8_opts $@; }
    fi
else
    function _pep8 () { :; }
fi

if `which pylint 2>&1 > /dev/null`; then
    pylint_opt="--disable=locally-disabled"
    test -f ${curdir}/pylintrc && \
        pylint_opt="$pylint_opt --rcfile=$curdir/pylintrc" || :
    function _pylint () { pylint ${rcopt} $@ || :; }
else
    function _pylint () { :; }
fi

if test $# -gt 0; then
    for x in $@; do _pep8 ${x%%:*}; _pylint ${x%%:*}; done
    PYTHONPATH=$topdir nosetests ${nosetests_opts} $@
else
    cd ${topdir}
    # Find out python package dir and run tests for .py files under it.
    for d in ./*; do
        if test -d $d -a -f $d/__init__.py -a "$d" != "./.tox"; then
            pypkgdir=$d

            for f in $(find ${pypkgdir} -name '*.py'); do
                echo "[Info] Check $f..."
                _pep8 $f
            done
            _pylint $d
            _pep8 $d
        fi
    done
    PYTHONPATH=. nosetests ${nosetests_opts} --all-modules
fi

# vim:sw=4:ts=4:et:
