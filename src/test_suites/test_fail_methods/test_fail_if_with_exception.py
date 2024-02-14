"""
Test class for testing the fail_if method.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestFailIfWithException(TestSuite):
    """ Test if the fail_if generates an exception and makes the test suite fail. """

    CLASSIFICATION = Classification.FAIL

    def test_fail_if(self):
        """ Make the test fail with exception. """
        self.fail_if(True, "This should generate an exception")


if __name__ == "__main__":

    TestFailIfWithException().run()
