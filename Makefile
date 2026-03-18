PYTHON := $(shell if [ -x ./.venv/bin/python ]; then echo ./.venv/bin/python; else echo python3; fi)

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	PYTHONPATH=src $(PYTHON) -m pytest

lint:
	$(PYTHON) -m compileall src tests

run-basic:
	PYTHONPATH=src $(PYTHON) -m synapse_engine.cli validate examples/basic_patch.yaml

run-demo:
	PYTHONPATH=src $(PYTHON) -m synapse_engine.cli demo basic
