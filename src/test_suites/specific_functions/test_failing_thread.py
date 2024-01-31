"""
Test the threading feature.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestThreading(TestSuite):

    CLASSIFICATION = Classification.FAIL

    def thread(self):
        self.sleep(0.5)
        # This will make the thread fail and the test suite should report a failure
        _a = 1 / 0

    def test_threading(self):
        t = self.start_thread(self.thread)
        self.fail_if(not t.is_alive(), "The thread is not running")

        while t.is_alive():
            self.sleep(0.1)


if __name__ == "__main__":

    TestThreading().run()
