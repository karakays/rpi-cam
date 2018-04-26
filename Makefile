PYTHON		= python3
VERSION_TXT	= VERSION
VERSION		= $(shell cat $(VERSION_TXT))

versionis:
	@echo "Version is" $(VERSION)

clean: clean-build clean-pyc

clean-build:
	sudo rm -fr build/
	sudo rm -fr dist/
	sudo rm -fr *.egg-info

clean-pyc:
	sudo find . -name '*.pyc' -exec rm -f {} +
	sudo find . -name '*.pyo' -exec rm -f {} +
	sudo find . -name __pycache__ -delete

build:
	$(PYTHON) setup.py bdist_wheel
