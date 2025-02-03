# PythonTemplate

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://img.shields.io/github/license/gvatsal60/PythonTemplate)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/gvatsal60/PythonTemplate/master.svg)](https://results.pre-commit.ci/latest/github/gvatsal60/PythonTemplate/HEAD)
[![CodeFactor](https://www.codefactor.io/repository/github/gvatsal60/PythonTemplate/badge)](https://www.codefactor.io/repository/github/gvatsal60/PythonTemplate)
![GitHub pull-requests](https://img.shields.io/github/issues-pr/gvatsal60/PythonTemplate)
![GitHub Issues](https://img.shields.io/github/issues/gvatsal60/PythonTemplate)
![GitHub forks](https://img.shields.io/github/forks/gvatsal60/PythonTemplate)
![GitHub stars](https://img.shields.io/github/stars/gvatsal60/PythonTemplate)

This repository serves as a foundational template for new python projects,
equipped with essential tools for maintaining code quality and documentation consistency.
It includes:

1. README.md
2. LICENSE
3. .gitignore
4. CODE_OF_CONDUCT.md
5. CONTRIBUTING.md
6. FUNDING.yml
7. CHANGELOG.md

## Table of Contents

1. [Getting Started](#getting-started)
2. [Build](#build)
3. [Run](#run)
4. [Testing](#testing)
5. [Cleaning](#cleaning)

## Getting Started

To get started with the project, ensure you have `Python 3` installed on your system.

## Build

To create virtualenv and install requirements for the project, run the following command:

```sh
make build
```

## Run

To run the main file, use the following command:

```sh
make run
```

You can also specify a particular file to run by adding the FILE variable:

Note: Path need to be mentioned if it's in a directory

```sh
make run FILE=file_name.py
or
make run FILE=app/app.py
```

## Testing

To run the tests, use the following command:

```sh
make test
```

You can also specify a particular file to test by adding the FILE variable:

Note: Path need to be mentioned if it's in a directory

```sh
make test FILE=file_name.py
```

## Cleaning

To clean the project directory, removing all compiled Python files, use the following command:

```sh
make clean
```

## Contributing

Contributions are welcome! Please read our
[Contribution Guidelines](https://github.com/gvatsal60/PythonTemplate/blob/HEAD/CONTRIBUTING.md)
before submitting pull requests.

## License

This project is licensed under the Apache License 2.0 License -
see the [LICENSE](https://github.com/gvatsal60/PythonTemplate/blob/HEAD/LICENSE)
file for details.
