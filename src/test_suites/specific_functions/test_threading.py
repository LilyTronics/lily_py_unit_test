"""
Test the threading feature.
"""

import lily_unit_test
import time


class TestThreading(lily_unit_test.TestSuite):

    def thread(self):
        for i in range(20):
            self.sleep(0.1)

    def test_threading(self):
        t = self.start_thread(self.thread)
        self.fail_if(not t.is_alive(), "The thread is not running")

        start = time.perf_counter()
        while t.is_alive():
            self.sleep(0.1)
        duration = time.perf_counter() - start
        self.log.debug("The thread took: {:.2f} seconds".format(duration))
        self.fail_if(abs(duration - 2) > 0.2, "Duration of the thread is not correct, should be 2 seconds")


if __name__ == "__main__":

    TestThreading().run()
