"""
Test class for testing a failing setup because of exception.
"""

from lily_unit_test.models.classification import Classification
from lily_unit_test.models.test_suite import TestSuite


class TestClassSetupFailException(TestSuite):

    CLASSIFICATION = Classification.FAIL

    def setup(self):
        _a = 1 / 0

    def test_dummy(self):
        return True


if __name__ == '__main__':

    TestClassSetupFailException().run()
