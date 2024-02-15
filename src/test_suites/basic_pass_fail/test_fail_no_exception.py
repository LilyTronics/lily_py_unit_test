"""
Test class for testing failing tests.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestFailNoException(TestSuite):
    CLASSIFICATION = Classification.FAIL

    def test_fail_by_return_false(self):
        return False


if __name__ == "__main__":

    TestFailNoException().run()
