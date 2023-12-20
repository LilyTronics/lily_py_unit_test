"""
Test class for use with the unit test.
"""

from lily_unit_test.models.test_suite import TestSuite


class TestClassPass(TestSuite):

    def test_01_pass_by_return_none(self):
        return None

    def test_02_pass_by_return_true(self):
        return True


if __name__ == '__main__':

    TestClassPass().run()
