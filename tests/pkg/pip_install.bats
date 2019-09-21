#! /usr/bin/bats
#
# Usage:
#   [PIP_TARGET_DIR=/tmp/i] $0
#
# Example:
#
# ssato@fc30% ./tests/pkg/pip_install.bats
# ✓ Test required packages are installed
# ✓ Test extra required package is installed
# ✓ Test extra required packages are installed
#
# 3 tests, 0 failures
# ssato@fc30%
#

SRCDIR=${SRCDIR:-.}
TDIR=${PIP_TARGET_DIR:-}

# TODO: Resolve deps automatically
# DEVEL_DEPS="$(sed -nr '/^devel =/,/^.options.packages.find/s/[[:blank:]]+([a-zA-Z0-9]+).*/\1/p' setup.cfg)"
DEVEL_DEPS="${DEVEL_DEPS:-coveralls flake8 mock nose pylint pycodestyle}"

function setup () {
    [[ -n ${TDIR} ]] || TDIR=$(mktemp --directory)
}

function teardown () {
    [[ ${TDIR:?} != '/' ]] && {
        :  # rm -rf ${TDIR}
    } || :
}

@test "Test required packages are installed" {
    run pip3 install -U -t ${TDIR} ${SRCDIR:?}
    run echo ${TDIR}/anyconfig*.dist-info;
    [[ ${status} -eq 0 ]]

    [[ -d ${TDIR}/anyconfig ]]
    [[ -d ${TDIR}/setuptools ]]

    run echo ${TDIR}/setuptools*.dist-info
    [[ ${status} -eq 0 ]]
}

@test "Test extra required package is installed" {
    run pip3 install -U -t ${TDIR} ${SRCDIR}'[toml]'
    run echo ${TDIR}/anyconfig*.dist-info;
    [[ ${status} -eq 0 ]]

    [[ -d ${TDIR}/anyconfig ]]
    [[ -d ${TDIR}/toml ]]

    run echo ${TDIR}/toml*.dist-info
    [[ ${status} -eq 0 ]]
}

@test "Test extra required packages are installed" {
    run pip3 install -U -t ${TDIR} ${SRCDIR}'[devel]'
    run echo ${TDIR}/anyconfig*.dist-info;
    [[ ${status} -eq 0 ]]

    [[ ${status} -eq 0 ]]
    [[ -d ${TDIR}/anyconfig ]]

    for erp in ${DEVEL_DEPS:?}; do
        run echo ${TDIR}/{erp}*
        echo "status = ${status}"
        echo "output = ${output}"
        [[ ${status} -eq 0 ]]
    done
}

# vim:sw=4:ts=4:et:
