# Makefile for ParserApp

# Variables
PYTHON = python3
VENV_DIR = venv
PIP = $(VENV_DIR)/bin/pip
PYTHON_VENV = $(VENV_DIR)/bin/python

# Default target
.PHONY: help
help:
	@echo "ParserApp - Available targets:"
	@echo "  venv      - Create virtual environment"
	@echo "  install   - Install dependencies"
	@echo "  run       - Run the main script"
	@echo "  clean     - Clean up generated files"
	@echo "  setup     - Complete setup (venv + install)"
	@echo "  all       - Setup and run"

# Create virtual environment
.PHONY: venv
venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created in $(VENV_DIR)/"

# Install dependencies
.PHONY: install
install: venv
	@echo "Installing dependencies..."
	@if [ -s requirements.txt ] && [ -n "$$(grep -v '^#' requirements.txt | grep -v '^$$')" ]; then \
		$(PIP) install -r requirements.txt --timeout 30; \
	else \
		echo "No dependencies to install."; \
	fi
	@echo "Dependencies installation complete."

# Run the main script
.PHONY: run
run: venv
	@echo "Running ParserApp..."
	$(PYTHON_VENV) main.py

# Complete setup
.PHONY: setup
setup: venv install

# Setup and run
.PHONY: all
all: setup run

# Clean up
.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR)
	rm -rf __pycache__
	rm -rf output
	rm -rf *.pyc
	@echo "Cleanup complete."