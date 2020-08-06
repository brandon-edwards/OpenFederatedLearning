# Copyright (C) 2020 Intel Corporation
# Licensed subject to the terms of the separately executed evaluation license agreement between Intel Corporation and you.

# Docker support removed from Makefile for now

python_version ?= python3.6

whl = dist/tfedlrn-0.0.0-py3-none-any.whl
tfl = venv/lib/$(python_version)/site-packages/tfedlrn

.PHONY: wheel
wheel: $(whl)

.PHONY: install
install: $(tfl)

.PHONY: venv
venv: venv/bin/python3

venv/bin/python3:
	$(python_version) -m venv venv
	# specifying pip version to avoid issue with later intel-tensorflow install
	venv/bin/pip3 install --force-reinstall pip==19.0
	venv/bin/pip3 install --upgrade setuptools
	venv/bin/pip3 install --upgrade wheel
	venv/bin/pip3 install --upgrade pyyaml

$(whl): venv/bin/python3
	venv/bin/python3 setup.py bdist_wheel
	# we will use the wheel, and do not want the egg info
	rm -r -f tfedlrn.egg-info

$(tfl): $(whl)
	venv/bin/pip3 install $(whl)

uninstall:
	venv/bin/pip3 uninstall -y tfedlrn
	rm -rf dist
	rm -rf build

.PHONY: reinstall
reinstall: uninstall install

clean:
	rm -r -f venv
	rm -r -f dist
	rm -r -f build
