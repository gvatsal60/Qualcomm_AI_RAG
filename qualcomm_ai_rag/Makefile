include ../cfg/.env

PYTHON := python3

SRC_DIR := src
TEST_DIR := tests
VENV_DIR := ../.venv

RMDIR:=rm -rf
VENV_PYTHON:=$(VENV_DIR)/bin/python
VENV_ACTIVATE:=$(VENV_DIR)/bin/activate

MAIN_PY := main.py

.PHONY: all build test clean

all:

build:
	@echo "Building project..."
	@$(SHELL) -c "../scripts/env_setup.sh"

test:
	@echo "Building tests..."
	@if [ -z "$(FILE)" ]; then $(VENV_PYTHON) -m unittest discover -v $(TEST_DIR) "*_test.py"; \
	else $(VENV_PYTHON) -m unittest -v $(TEST_DIR)/$$FILE; fi

run: build
	@echo "Running project..."
	@if [ -z "$(FILE)" ]; then FILE=$(MAIN_PY); fi; \
	. $(VENV_ACTIVATE) && \
	streamlit run $(SRC_DIR)/$$FILE

clean:
	@echo "Cleaning project..."
	@$(RMDIR) $(VENV_DIR) \
		$(SRC_DIR)/__pycache__ \
		$(TEST_DIR)/__pycache__
