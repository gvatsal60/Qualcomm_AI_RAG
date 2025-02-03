"""
This script provides functionality to create and activate a Python virtual
environment.
"""

import os
import subprocess
import sys


def create_and_activate_venv():
    """
    Creates a Python virtual environment in the current directory, installs the
    required packages from a requirements.txt file, and prints the command to
    activate the virtual environment.

    The function performs the following steps:
    1. Determines the correct command for creating a virtual environment.
    2. Creates the virtual environment in a directory named '.venv'.
    3. Installs the required packages listed in 'requirements.txt' inside the
       virtual environment.
    4. Prints the command to activate the virtual environment to the console.

    If any step fails, the function prints an error message and exits the
    program with a non-zero status code.

    Note:
      This function assumes that 'requirements.txt' is present in the current
      directory.

    Raises:
      subprocess.CalledProcessError: If an error occurs while creating the
                       virtual environment or installing the
                       requirements.
    """
    sys_exec = sys.executable
    venv_dir = '.venv'

    # Determine the correct command for creating a virtual environment
    venv_command = [sys_exec, '-m', 'venv', venv_dir]

    # Create the virtual environment
    try:
        subprocess.run(venv_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating virtual environment: {e}")
        sys.exit(1)

    # Install the requirements inside the virtual environment
    requirements_file = 'requirements.txt'
    pip_install_command = (
        f'pip install --upgrade --no-cache-dir -r {requirements_file}'
    )

    if os.name == 'nt':  # Windows
        venv_pip_install_command = (
            rf'.\{venv_dir}\Scripts\python.exe -m {pip_install_command}'
        )
    else:  # Linux and MacOS
        venv_pip_install_command = (
            f'./{venv_dir}/bin/python -m {pip_install_command}'
        )

    try:
        subprocess.run(venv_pip_install_command.split(), check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing requirements: {e}")
        sys.exit(1)


if __name__ == '__main__':
    create_and_activate_venv()
