#!/usr/bin/make
HOOKS_DIR := $(PWD)/hooks
TEST_PREFIX := PYTHONPATH=$(HOOKS_DIR)
IGNORE_ERRORS := E402,F401
# E402 module level import not at top of file
# F401 module imported but unused

lint: 
	flake8 --ignore=$(IGNORE_ERRORS) hooks tests
	charm proof

scripts/charm_helpers_sync.py:
	bzr cat lp:charm-helpers/tools/charm_helpers_sync/charm_helpers_sync.py \
	    > $@

sync: scripts/charm_helpers_sync.py
	python $< -c charm-helpers.yaml
