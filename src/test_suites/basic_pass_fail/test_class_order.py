"""
Test class for testing the order of execution.
"""

from lily_unit_test.models.test_suite import TestSuite


class TestClassOrder(TestSuite):

    ORDER = []

    def setup(self):
        del self.ORDER[:]

    def test_first(self):
        self.ORDER.append(0)

    def test_second(self):
        self.ORDER.append(1)

    def test_third(self):
        self.ORDER.append(2)

    def test_fourth(self):
        self.ORDER.append(3)

    def test_order(self):
        self.log.debug("Order: {}".format(self.ORDER))
        for i, j in enumerate(self.ORDER):
            self.fail_if(i != j, "Test order is not correct for index {}, value {}".format(i, j))


if __name__ == "__main__":

    TestClassOrder().run()
