# ref. https://docs.pagure.org/copr.copr/user_documentation.html#scm
#      ('make srpm' section)

makefile_dir := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
outdir ?= $(makefile_dir)/../dist

srpm:
	dnf install -y tox python3
	python3 setup.py bdist_rpm --source-only --dist-dir=$(outdir)

.PHONY: srpm
