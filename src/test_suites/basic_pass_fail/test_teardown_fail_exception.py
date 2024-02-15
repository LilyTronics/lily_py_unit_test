"""
Test class for testing a failing teardown because of an exception.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestTeardownFailException(TestSuite):
    CLASSIFICATION = Classification.FAIL

    def test_dummy(self):
        return True

    def teardown(self):
        _ = 1 / 0


if __name__ == "__main__":

    TestTeardownFailException().run()
