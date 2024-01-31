"""
Test class for testing the fail method.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestFailNoException(TestSuite):

    CLASSIFICATION = Classification.FAIL

    def test_fail(self):
        self.fail("This should not generate an exception, but should fail", False)


if __name__ == "__main__":

    TestFailNoException().run()
