#! /bin/bash
set -ex

curdir=${0%/*}
docdir=${curdir}/../docs
output=${curdir}/../README.rst
readme_files="
${curdir}/header.rst
${docdir}/introduction.rst
"
# ${docdir}/hacking.rst
rst2html=$(which rst2html 2> /dev/null > /dev/null && echo rst2html || echo rst2html-3)

cat ${readme_files} > ${output}
${rst2html} ${output} > /dev/null

# vim:sw=2:ts=2:et:
