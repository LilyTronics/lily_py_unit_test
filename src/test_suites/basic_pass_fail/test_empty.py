"""
Test class for testing an empty test suite.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestEmpty(TestSuite):
    """ Test if an empty class fails because there are no test methods. """

    CLASSIFICATION = Classification.FAIL


if __name__ == "__main__":

    TestEmpty().run()
