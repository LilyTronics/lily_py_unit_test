"""
This example shows how to run a simple unit test.
"""

import lily_unit_test


class MyClass(object):
    """
    Your class that will do something amazing.
    """

    @staticmethod
    def add_one(x):
        return x + 1

    @staticmethod
    def add_two(x):
        return x + 2


class MyTestSuite(lily_unit_test.TestSuite):
    """
    The test suite for testing MyClass.
    """

    @staticmethod
    def test_add_one():
        assert MyClass.add_one(3) == 4, "Wrong return value"

    @staticmethod
    def test_add_two():
        assert MyClass.add_two(3) == 5, "Wrong return value"


if __name__ == "__main__":
    """
    Run the test code, when not imported.
    """

    MyTestSuite().run()
