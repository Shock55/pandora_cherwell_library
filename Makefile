all: monlib
.PHONY: all monlib install uninstall
lib_dir=/opt/monlib
log_file=/var/log/monlib.log
conf_dir=/etc/monlib
venv=$(lib_dir)/venv

install:
	@echo install the library files..
	mkdir -p $(lib_dir)
	mkdir $(conf_dir)
	touch $(log_file)
	cp -r monlib $(lib_dir)
	cp -r config $(conf_dir)
	chown root:root $(lib_dir)/*
	chmod -R 644 $(lib_dir)/*
	chmod -R 755 $(lib_dir)/*
	@echo Creating python virtual env and installing packages..
	python3 -m venv $(venv)
	$(venv)/bin/pip3 install --upgrade pip
	$(venv)/bin/pip3 install -e $(lib_dir)/monlib/.
	@echo Installation complete

uninstall:
	-rm -rf $(conf_dir)
	-rm -rf $(lib_dir)
	-rm -f $(log_file)
