# Makefile for development.
# See INSTALL and docs/dev.txt for details.
VENV := $(shell echo $${VIRTUAL_ENV-var/venv})
ROOT_DIR = $(shell pwd)
BIN_DIR = $(VENV)/bin
PYTHON=$(BIN_DIR)/python
PIP = $(BIN_DIR)/pip
NOSE = $(BIN_DIR)/nosetests
PROJECT = $(shell $(PYTHON) -c "import setup; print setup.NAME")

install: develop

develop:
	@mkdir -p $(ROOT_DIR)/var
	virtualenv $(VENV)
	$(PYTHON) setup.py develop
	$(PIP) install nose rednose docutils coverage sphinxcontrib-testbuild flake8

clean:
	find $(ROOT_DIR)/ -name "*.pyc" -delete
	find $(ROOT_DIR)/ -name ".noseids" -delete


distclean: clean
	rm -rf $(ROOT_DIR)/*.egg-info


test: test-app test-pep8


test-app:
	@mkdir -p $(ROOT_DIR)/var/test/
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
	$(PIP) install zest.releaser
	$(BIN_DIR)/fullrelease
