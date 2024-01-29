"""
Test class for testing passing tests.
"""

from lily_unit_test.test_suite import TestSuite


class TestPass(TestSuite):

    def test_pass_by_return_none(self):
        return None

    def test_pass_by_return_true(self):
        return True


if __name__ == "__main__":

    TestPass().run()
