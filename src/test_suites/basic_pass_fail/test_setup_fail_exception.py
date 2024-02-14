"""
Test class for testing a failing setup because of exception.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestSetupFailException(TestSuite):
    """ Test if the setup fails when generating an exception. """

    CLASSIFICATION = Classification.FAIL

    def setup(self):
        """ Make the setup fail by generation an exception. """
        _a = 1 / 0

    def test_dummy(self):
        """ Dummy method because a test method is needed. """
        return True


if __name__ == "__main__":

    TestSetupFailException().run()
