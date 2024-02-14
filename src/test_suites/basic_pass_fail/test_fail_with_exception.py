"""
Test class for testing failing tests.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestFailWithException(TestSuite):
    """ Test failing of the test suite by raising an exception. """

    CLASSIFICATION = Classification.FAIL

    def test_fail_by_return_false(self):
        """ Make the test fail by raising an exception. """
        _ = 1 / 0


if __name__ == "__main__":

    TestFailWithException().run()
