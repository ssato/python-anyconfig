#! /usr/bin/bats
#
# Usage:
#   [PIP_TARGET_DIR=/tmp/i] $0
#
# Example:
#
# [ssato@f30]/tmp/ac-test% ./tests/pkg/extra_requires.bats
#  ✓ Test the configuration file with using dhcpd
#
#  1 test, 0 failures
#  [ssato@f30]

TDIR=
# DEVEL_ERPS="$(sed -nr '/^devel =/,/^.options.packages.find/s/[[:blank:]]+([a-zA-Z0-9]+).*/\1/p' setup.cfg)"
DEVEL_ERPS="coveralls flake8 mock nose pylint pycodestyle"

function setup () {
    TDIR=$(mktemp --directory)
}

function teardown () {
    [[ ${TDIR:?} != '/' ]] && {
        :  # rm -rf ${TDIR}
    } || :
}

@test "Test required packages are installed" {
    run pip3 install -U -t ${TDIR} .
    run echo ${TDIR}/anyconfig*.dist-info; 
    [[ ${status} -eq 0 ]]

    [[ -d ${TDIR}/anyconfig ]]
    [[ -d ${TDIR}/setuptools ]]

    run echo ${TDIR}/setuptools*.dist-info
    [[ ${status} -eq 0 ]]
}

@test "Test extra required package is installed" {
    run pip3 install -U -t ${TDIR} '.[toml]'
    run echo ${TDIR}/anyconfig*.dist-info; 
    [[ ${status} -eq 0 ]]

    [[ -d ${TDIR}/anyconfig ]]
    [[ -d ${TDIR}/toml ]]

    run echo ${TDIR}/toml*.dist-info
    [[ ${status} -eq 0 ]]
}

@test "Test extra required packages are installed" {
    run pip3 install -U -t ${TDIR} '.[devel]'
    run echo ${TDIR}/anyconfig*.dist-info; 
    [[ ${status} -eq 0 ]]

    [[ ${status} -eq 0 ]]
    [[ -d ${TDIR}/anyconfig ]]

    for erp in ${DEVEL_ERPS:?}; do
        run echo ${TDIR}/{erp}*
        echo "status = ${status}"
        echo "output = ${output}"
        [[ ${status} -eq 0 ]]
    done
}

# vim:sw=4:ts=4:et:
