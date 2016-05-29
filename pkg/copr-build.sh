#! /bin/bash
# Build SRPM and submit new build to copr.
#
# References:
# - https://developer.fedoraproject.org/deployment/copr/copr-cli.html
# - http://copr-rest-api.readthedocs.io/en/latest/Resources/build.html#submit-new-build
#
set -ex

curdir=${0%/*}
topdir=${curdir}/../
srpmdir=${topdir}/dist

copr_project=ssato/python-anyconfig
srpm=$(ls -1 ${srpmdir:?}/*.src.rpm | sort -Vr | head -n 1)  # FIXME

test -f ~/.config/copr
copr-cli build ${copr_project:?} ${srpm:?}

# vim:sw=4:ts=4:et:
