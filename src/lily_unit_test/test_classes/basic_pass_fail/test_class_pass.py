"""
Test class for testing passing tests.
"""

from lily_unit_test.models.test_suite import TestSuite


class TestClassPass(TestSuite):

    def test_pass_by_return_none(self):
        return None

    def test_pass_by_return_true(self):
        return True


if __name__ == '__main__':

    TestClassPass().run()
