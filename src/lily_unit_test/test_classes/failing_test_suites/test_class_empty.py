"""
Test class for use with the unit test.
"""

from lily_unit_test.models.test_suite import TestSuite


class TestClassEmpty(TestSuite):
    pass


if __name__ == '__main__':

    TestClassEmpty().run()
