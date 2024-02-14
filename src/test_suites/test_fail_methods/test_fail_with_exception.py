"""
Test class for testing the fail method.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestFailWithException(TestSuite):
    """ Test if the fail generates an exception and makes the test suite fail. """

    CLASSIFICATION = Classification.FAIL

    def test_fail(self):
        """ Make the test fail with exception. """
        self.fail("This should generate an exception")


if __name__ == "__main__":

    TestFailWithException().run()
