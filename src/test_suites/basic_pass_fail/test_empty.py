"""
Test class for testing an empty test suite.
"""

from lily_unit_test.models.classification import Classification
from lily_unit_test.models.test_suite import TestSuite


class TestEmpty(TestSuite):

    CLASSIFICATION = Classification.FAIL


if __name__ == "__main__":

    TestEmpty().run()
