from doctest import DocTestSuite
from unittest import TestLoader, TestSuite

from misclib import metaclasses


def load_tests(loader: TestLoader, tests: TestSuite, pattern: str, /) -> TestSuite:
    suite = DocTestSuite(metaclasses, globs={'__name__': '__main__'})
    suite.addTests(tests)
    return suite
