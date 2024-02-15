"""
Test class for testing the fail method.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestFailWithException(TestSuite):
    CLASSIFICATION = Classification.FAIL

    def test_fail(self):
        self.fail("This should generate an exception")


if __name__ == "__main__":

    TestFailWithException().run()
