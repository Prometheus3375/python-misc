# Development

## Installation

1. Install [Python 3.12.8](https://www.python.org/downloads/release/python-3128/)
   or a higher version of Python 3.12.
2. Run `python -m pip install -U pip setuptools wheel` to update pip, setuptools and wheel packages.

## Running tests

1. Open terminal in the root of this project.
2. Run `python -m unittest discover -v tests "test_*.py"` to execute all tests.

Base tests for `misclib.utils.color` include only a fraction of all possible colors.
Run `python -m unittest -v tests.test_color.TestColorFull`
to execute tests on all possible colors.
When using PyCharm test configurations,
specify environmental variable `TEST_COLOR_FULL` with any non-empty value
to run tests on all possible colors.
