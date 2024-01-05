"""
Test class for testing a failing teardown because of an exception.
"""

from lily_unit_test.models.classification import Classification
from lily_unit_test.models.test_suite import TestSuite


class TestClassTeardownFailException(TestSuite):

    CLASSIFICATION = Classification.FAIL

    def test_dummy(self):
        return True

    def teardown(self):
        _a = 1 / 0


if __name__ == '__main__':

    TestClassTeardownFailException().run()
