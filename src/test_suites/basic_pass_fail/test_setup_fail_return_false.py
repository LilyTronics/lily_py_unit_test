"""
Test class for testing a failing setup because of returning False.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestSetupFailReturnFalse(TestSuite):
    """ Test if the setup fails when it returns False. """

    CLASSIFICATION = Classification.FAIL

    def setup(self):
        """ Setup returns false to make the test suite fail. """
        return False

    def test_dummy(self):
        """ Dummy test method needed to make the test suite run. """
        return True


if __name__ == "__main__":

    TestSetupFailReturnFalse().run()
