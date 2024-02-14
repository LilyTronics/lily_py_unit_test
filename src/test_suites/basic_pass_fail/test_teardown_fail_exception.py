"""
Test class for testing a failing teardown because of an exception.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestTeardownFailException(TestSuite):
    """ Test if the test suite fails if an exception was raised in the teardown. """

    CLASSIFICATION = Classification.FAIL

    def test_dummy(self):
        """ Dummy test method is needed to make the test suite run. """
        return True

    def teardown(self):
        """ Generate an exception in the teardown. """
        _ = 1 / 0


if __name__ == "__main__":

    TestTeardownFailException().run()
