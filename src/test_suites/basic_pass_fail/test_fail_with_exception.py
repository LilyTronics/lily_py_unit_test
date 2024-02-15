"""
Test class for testing failing tests.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestFailWithException(TestSuite):
    CLASSIFICATION = Classification.FAIL

    def test_fail_by_return_false(self):
        _ = 1 / 0


if __name__ == "__main__":

    TestFailWithException().run()
