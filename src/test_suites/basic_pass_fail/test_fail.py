"""
Test class for testing failing tests.
"""

from lily_unit_test.models.classification import Classification
from lily_unit_test.models.test_suite import TestSuite


class TestFail(TestSuite):

    CLASSIFICATION = Classification.FAIL

    def test_fail_by_return_false(self):
        return False

    def test_fail_by_exception(self):
        _a = 1 / 0


if __name__ == "__main__":

    TestFail().run()
