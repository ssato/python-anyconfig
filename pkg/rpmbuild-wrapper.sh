#! /bin/bash
#
# Simple wrapper script for rpmbuild to build *rpm w/ minimum side effects,
# e.g. creating ~/rpmbuild/{RPMS,SOURCES,BUILD,...}.
#
# Author: Satoru SATOH <satoru.satoh at gmail.com>
# License: MIT
set -e

rpmspec=
workdir=.
buildstep=s
verbose=0
usage="Usage: $0 [OPTIONS] RPMSPEC"

function show_help () {
  cat <<EOH
$usage
Options:
  -w WORKDIR  Top directory to make working dirs and files [${workdir:?}]
  -s STEP     A char represents build step passed to rpmbuild's -b option.
              See rpmbuild(8) also. [${buildstep:?}]

  -h          Show this help and exit.
  -v          Verbose mode.

Examples:
 $0 foo.spec
 $0 -w \$(mktemp -d) bar.spec
 $0 -w \$(mktemp -d) -v -s b baz.spec
EOH
}

# see also: rpmbuild(8), /usr/lib/rpm/macros
function _rpmbuild () {
  local buildstep=$1
  local workdir=$2
  local rpmspec=$3

  rpmbuild -b${buildstep} \
    --define "_topdir ${workdir}" \
    --define "_rpmdir ${workdir}" \
    --define "_sourcedir ${workdir}" \
    --define "_specdir ${workdir}" \
    --define "_srcrpmdir ${workdir}" \
    --define "_builddir ${workdir}" \
    --define "_buildrootdir ${workdir}" \
    ${rpmspec:?}
}

while getopts "w:s:hv" opt
do
  case $opt in
    w) workdir=$OPTARG ;;
    s) buildstep=$OPTARG ;;
    v) verbose=1 ;;
    h) show_help; exit 0 ;;
    \?) show_help; exit 1 ;;
  esac
done
shift $(($OPTIND - 1))

function vecho () {
  (test "x$verbose" = "x1" && echo $@ || echo -ne "" )
}

if test $# -lt 1; then
  echo "$usage"
  exit 1
fi
rpmspec=$1  # or ${1:-package.spec} (fallbacked to 'package.spec') ?

if which rpmbuild 2>/dev/null 1>/dev/null; then
  :
else
  echo "rpmbuild is NOT found in your PATH! Aborting..."
  exit 1
fi

if test ! -f ${rpmspec}; then
  echo "RPMSPEC ${rpmspec} does not exist!"
  exit 1
fi

if test ! -d ${workdir}; then
  vecho "Making working dir: ${workdir}"
  mkdir -p ${workdir}
fi

_rpmbuild ${buildstep:?} ${workdir:?} ${rpmspec:?}

# vim:sw=2:ts=2:et:
