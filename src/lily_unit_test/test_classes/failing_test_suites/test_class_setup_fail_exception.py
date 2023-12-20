"""
Test class for use with the unit test.
"""

from lily_unit_test.models.test_suite import TestSuite


class TestClassSetupFailException(TestSuite):

    def setup(self):
        _a = 1 / 0

    def test_dummy(self):
        return True


if __name__ == '__main__':

    TestClassSetupFailException().run()
