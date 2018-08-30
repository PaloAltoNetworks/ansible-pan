MODULES_DIR   = modules
FORMATTER = hacking/module_formatter.py

modulesasrst:
	mkdir modules
	$(FORMATTER) -v -M ../library/ -o modules/ -T hacking/templates/ -t rst -I modules.rst

modulesasmd: $(MODULES_DIR)
	$(FORMATTER) -v -M ../library/ -o modules/ -T hacking/templates/ -t md -I modules.rst

cleanmodules:
	@rm -rf modules library.rst

$(MODULES_DIR):
	test ! -d $(MODULES_DIR) && mkdir $(MODULES_DIR)
