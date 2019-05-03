# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
ANSIBLEDIR    = ../../ansible

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

build:
	rm -rf /tmp/modules && mkdir /tmp/modules
	PYTHONPATH=$(ANSIBLEDIR)/lib $(ANSIBLEDIR)/docs/bin/plugin_formatter.py -M ../library -o /tmp/modules/ -T $(ANSIBLEDIR)/docs/templates/ -t rst
	rm -rf modules/*
	mv /tmp/modules/panos_* modules
	for x in $$(ls -1 modules/panos_*_module.rst); do python tidyrst.py $$x ; done
	python mkmodref.py
	rm -rf /tmp/modules

fullbuild: build
	rm -rf _build/*
	make html

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
