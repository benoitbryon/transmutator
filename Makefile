# Makefile for development.
# See INSTALL and docs/dev.txt for details.
SHELL = /bin/bash
ROOT_DIR = $(shell pwd)
BIN_DIR = $(ROOT_DIR)/bin
DATA_DIR = $(ROOT_DIR)/var
WGET = wget
BUILDOUT_CFG = $(ROOT_DIR)/etc/buildout.cfg
BUILDOUT_DIR = $(ROOT_DIR)/lib/buildout
BUILDOUT_VERSION = 2.2.0
BUILDOUT_BOOTSTRAP_URL = https://raw.github.com/buildout/buildout/$(BUILDOUT_VERSION)/bootstrap/bootstrap.py
BUILDOUT_BOOTSTRAP = $(BUILDOUT_DIR)/bootstrap.py
BUILDOUT_BOOTSTRAP_ARGS = -c $(BUILDOUT_CFG) --version=$(BUILDOUT_VERSION) buildout:directory=$(ROOT_DIR)
BUILDOUT = $(BIN_DIR)/buildout
BUILDOUT_ARGS = -N -c $(BUILDOUT_CFG) buildout:directory=$(ROOT_DIR)
VIRTUALENV_DIR = $(ROOT_DIR)/lib/virtualenv
PIP = $(VIRTUALENV_DIR)/bin/pip
NOSE = $(BIN_DIR)/nosetests
PYTHON = $(VIRTUALENV_DIR)/bin/python
PROJECT = $(shell $(PYTHON) -c "import setup; print setup.NAME")

configure:
	# Configuration is stored in etc/ folder. Not generated yet.


develop: buildout


py27:
	if [ ! -x $(PIP) ]; then virtualenv --no-site-packages $(VIRTUALENV_DIR); fi
	$(PIP) install -r $(ROOT_DIR)/etc/pip.cfg


buildout: py27
	if [ ! -d $(BUILDOUT_DIR) ]; then mkdir -p $(BUILDOUT_DIR); fi
	if [ ! -f $(BUILDOUT_BOOTSTRAP) ]; then wget -O $(BUILDOUT_BOOTSTRAP) $(BUILDOUT_BOOTSTRAP_URL); fi
	if [ ! -x $(BUILDOUT) ]; then $(PYTHON) $(BUILDOUT_BOOTSTRAP) $(BUILDOUT_BOOTSTRAP_ARGS); fi
	$(BUILDOUT) $(BUILDOUT_ARGS)


clean:
	find $(ROOT_DIR)/ -name "*.pyc" -delete
	find $(ROOT_DIR)/ -name ".noseids" -delete


distclean: clean
	rm -rf $(ROOT_DIR)/*.egg-info


maintainer-clean: distclean
	rm -rf $(BIN_DIR)/
	rm -rf $(ROOT_DIR)/lib/


test: test-app test-pep8


test-app:
	$(NOSE) -c $(ROOT_DIR)/etc/nose.cfg tests $(PROJECT)
	mv $(ROOT_DIR)/.coverage $(ROOT_DIR)/var/test/app.coverage


test-pep8:
	$(BIN_DIR)/flake8 $(PROJECT)


test-documentation:
	$(NOSE) -c $(ROOT_DIR)/etc/nose.cfg sphinxcontrib.testbuild.tests


documentation: sphinx-apidoc sphinx-html


# Remove auto-generated API documentation files.
# Files will be restored during sphinx-build, if "autosummary_generate" option
# is set to True in Sphinx configuration file.
sphinx-apidoc-clean:
	find docs/api/ -type f \! -name "index.txt" -delete


sphinx-apidoc: sphinx-apidoc-clean
	$(BIN_DIR)/sphinx-apidoc --output-dir $(ROOT_DIR)/docs/api/ --suffix txt $(PROJECT)


sphinx-html:
	if [ ! -d docs/_static ]; then mkdir docs/_static; fi
	make --directory=docs clean html doctest


release:
	$(BIN_DIR)/fullrelease
