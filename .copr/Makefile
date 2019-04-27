dist:
	mkdir -p $@

srpm: dist
	dnf -y install python3
	python3 setup.py bdist_rpm --source-only

.PHONY: srpm
