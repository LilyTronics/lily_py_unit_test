"""
Test class for testing the fail method.
"""

from lily_unit_test.models.classification import Classification
from lily_unit_test.models.test_suite import TestSuite


class TestFailIfWithException(TestSuite):

    CLASSIFICATION = Classification.FAIL

    def test_assert_if(self):
        self.fail('This should generate an exception')


if __name__ == '__main__':

    TestFailIfWithException().run()