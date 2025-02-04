#!/bin/bash

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please install 'python3' first."
    exit 1
fi

# Check if a virtual environment folder already exists
VENV_PATH="../.venv"

if [ -d "${VENV_PATH}" ]; then
    echo "Virtual environment '.venv' already exists."
else
    # Create a virtual environment
    if ! command -v uv &>/dev/null; then
        python3 -m venv ${VENV_PATH}
    else
        uv venv ${VENV_PATH}
    fi
    echo "Virtual environment '.venv' created."
fi

# Activate the virtual environment
source ${VENV_PATH}/bin/activate

# Find all 'requirements.txt' files in the current directory and subdirectories
REQUIREMENTS_FILES=$(find ../. -type f -name "requirements.txt")

# If any requirements.txt files are found, install packages
if [ -n "${REQUIREMENTS_FILES}" ]; then
    for REQUIREMENTS_FILE in ${REQUIREMENTS_FILES}; do
        if ! command -v uv &>/dev/null; then
            pip install -r "${REQUIREMENTS_FILE}"
        else
            uv pip install -r "${REQUIREMENTS_FILE}"
        fi
    done
    echo "Packages from all found 'requirements.txt' files installed."
    if command -v playwright &>/dev/null; then
        playwright install
        playwright install-deps
    fi
else
    echo "'requirements.txt' not found in the current directory or any subdirectories."
fi
