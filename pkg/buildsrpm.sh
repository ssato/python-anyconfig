#! /bin/bash
#
# Build source RPM from source and RPM SPEC file.
#
set -e -o pipefail

usage="Usage: $0 [NAME [RPMSPECIN [BUILDDIR [SRCDIR]]]]"

self=$0
selfdir="${self%/*}"

RPMSPECIN="${selfdir:?}/package.spec.in"

BUILDDIR="${selfdir}/../build"
SRCDIR="${selfdir}/../src"
DISTDIR="${selfdir}/../dist"

# Set or detect name.
NAME=${1}
[[ -z ${NAME} ]] && {
    NAME=$(sed -nr 's/^name.*=.*"(\S+)"$/\1/p' pyproject.toml)
    [[ -z ${NAME} ]] && {
        cat << EOM
[Error] No name was provided, and could not be automatically detected.
EOM
        echo "${usage}"
        exit 1
    } || :
}

RPMSPECIN=${2:-${RPMSPECIN}}
BUILDDIR=${3:-${BUILDDIR}}
SRCDIR=${4:-${SRCDIR}}
RELEASE=${5:-1}

test -f ${RPMSPECIN:?} && test -d ${SRCDIR:?} && test -d ${DISTDIR:?} || {
    echo "[Error] NOT found: ${RPMSPECIN} and/or ${SRCDIR} and/or ${DISTDIR}"
    echo "${usage}"
    exit 1
}

test -d ${BUILDDIR} || mkdir -p ${BUILDDIR}

# Detect version info.
candidates=$(
find ${SRCDIR} -type f -iregex '.*/__init__.py'
)

for f in ${candidates:?}
do
  VERSION=$(
    grep -q __version__ $f &&
    sed -nr 's/^__version__ = .(.+)./\1/p' $f || :
)
  [[ -z ${VERSION} ]] || break
done

[[ -z ${VERSION} ]] && {
    cat << EOM
[Error] Could NOT find version string from ${SRCDIR}/**/__init__.py
EOM
    exit 1
} || :

# Find src dist.
SRCDIST=$(ls -1 ${DISTDIR}/${NAME}-${VERSION}.*)
[[ -z ${SRCDIST} ]] && {
    echo "[Error] Cound NOT find src dist. Build it in advance."
} || :
cp -f ${SRCDIST} ${BUILDDIR}

# Generate the RPM SPEC file from ${RPMSPECIN}.
RPMSPECIN_fn=${RPMSPECIN##*/}
RPMSPEC=${BUILDDIR}/${RPMSPECIN_fn/.in/}

sed -r "
s/@NAME@/${NAME}/g
s/@VERSION@/${VERSION}/g
s/@RELEASE@/${RELEASE}/g
" ${RPMSPECIN} > ${RPMSPEC}

_rpmbuild () {
    rpmbuild --define "_topdir ${BUILDDIR}" \
        --define "_srcrpmdir ${BUILDDIR}" \
        --define "_sourcedir ${BUILDDIR}" \
        --define "_buildroot ${BUILDDIR}" \
        -bs $@
}

_rpmbuild ${RPMSPEC}
