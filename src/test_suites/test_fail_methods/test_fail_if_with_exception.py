"""
Test class for testing the fail_if method.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestFailIfWithException(TestSuite):

    CLASSIFICATION = Classification.FAIL

    def test_fail_if(self):
        self.fail_if(True, "This should generate an exception")


if __name__ == "__main__":

    TestFailIfWithException().run()
