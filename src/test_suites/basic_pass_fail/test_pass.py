"""
Test class for testing passing tests.
"""

from lily_unit_test.test_suite import TestSuite


class TestPass(TestSuite):
    """ Test suite that should always pass. """

    def test_pass_by_return_none(self):
        """ Test pass by returning None. """
        return None

    def test_pass_by_return_true(self):
        """ Test pass by returning True. """
        return True


if __name__ == "__main__":

    TestPass().run()
