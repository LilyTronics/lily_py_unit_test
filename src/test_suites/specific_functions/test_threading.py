"""
Test the threading feature.
"""

import time
import lily_unit_test


class TestThreading(lily_unit_test.TestSuite):
    """ Test the threading function of the test suite. """

    def _thread(self):
        for _ in range(20):
            self.sleep(0.1)

    def test_threading(self):
        """ Test the threading function. """
        t = self.start_thread(self._thread)
        self.fail_if(not t.is_alive(), "The thread is not running")
        start = time.perf_counter()
        while t.is_alive():
            self.sleep(0.1)
        duration = time.perf_counter() - start
        self.log.debug(f"The thread took: {duration:.2f} seconds")
        self.fail_if(abs(duration - 2) > 0.2,
                     "Duration of the thread is not correct, should be 2 seconds")


if __name__ == "__main__":

    TestThreading().run()
