"""
Test class for testing the fail_if method.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestFailIfNoException(TestSuite):

    CLASSIFICATION = Classification.FAIL

    def test_fail_if(self):
        self.fail_if(True, "This should not generate an exception, but should fail", False)


if __name__ == "__main__":

    TestFailIfNoException().run()
