"""
Test class for testing the fail method.
"""

from lily_unit_test.models.classification import Classification
from lily_unit_test.models.test_suite import TestSuite


class TestFailNoException(TestSuite):

    CLASSIFICATION = Classification.FAIL

    def test_fail(self):
        return self.fail('This should not generate an exception, but failing using the return value', False)


if __name__ == '__main__':

    TestFailNoException().run()
