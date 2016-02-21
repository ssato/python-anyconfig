#! /bin/bash
set -ex

curdir=${0%/*}
docdir=${curdir}/../docs
output=${curdir}/../README.rst
readme_files="
${docdir}/header.rst
${docdir}/introduction.rst
"
# ${docdir}/hacking.rst

cat ${readme_files} > ${output}
rst2html ${output} > /dev/null

# vim:sw=2:ts=2:et:
