from doctest import DocTestSuite
from unittest import TestLoader, TestSuite

from misclib import context


def load_tests(loader: TestLoader, tests: TestSuite, pattern: str, /) -> TestSuite:
    suite = DocTestSuite(context, globs={'__name__': '__main__'})
    suite.addTests(tests)
    return suite
