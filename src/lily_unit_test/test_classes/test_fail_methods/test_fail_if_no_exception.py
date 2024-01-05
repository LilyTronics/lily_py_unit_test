"""
Test class for testing the fail_if method.
"""

from lily_unit_test.models.classification import Classification
from lily_unit_test.models.test_suite import TestSuite


class TestFailIfNoException(TestSuite):

    CLASSIFICATION = Classification.FAIL

    def test_fail_if(self):
        return self.fail_if(True, 'This should not generate an exception, but failing using the return value', False)


if __name__ == '__main__':

    TestFailIfNoException().run()
