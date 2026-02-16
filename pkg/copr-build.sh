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
srpmdir=${topdir}/build

# see also
# - /etc/fedora-release
# - https://copr.fedorainfracloud.org/coprs/ssato/python-anyconfig/
dists="
fedora-42-x86_64
fedora-rawhide-x86_64
"

copr_project=ssato/python-anyconfig
srpm="$(ls -1 ${srpmdir:?}/*.src.rpm | sort -Vr | head -n 1)"  # FIXME

for dist in ${dists:?}; do
    mock -r ${dist:?} "${srpm:?}"
done

test -f ~/.config/copr
copr-cli build ${copr_project:?} "${srpm:?}"
