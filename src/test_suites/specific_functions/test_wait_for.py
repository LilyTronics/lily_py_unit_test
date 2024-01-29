"""
Test the wait for API.
"""

import lily_unit_test
import time


class TestWaitFor(lily_unit_test.TestSuite):

    _test_value = [False]

    def _change_value(self):
        self.sleep(0.5)
        self._test_value[0] = True

    def _update_value(self):
        self._test_value += 1
        return self._test_value

    def test_wait_for_variable(self):
        # Set initial value of the variable
        self._test_value[0] = False

        # We use a thread to manipulate the value independent of the wait for
        self.start_thread(self._change_value)

        start = time.perf_counter()
        result = self.wait_for(self._test_value, True, 1, 0.1)
        if result:
            duration = time.perf_counter() - start
            self.log.debug("It took {:.2f} seconds for the variable to change".format(duration))
        else:
            self.fail("The value did not change")

    def test_wait_for_function(self):
        # Set initial value of the variable
        self._test_value = 0

        start = time.perf_counter()
        result = self.wait_for(self._update_value, 5, 1, 0.1)
        if result:
            duration = time.perf_counter() - start
            self.log.debug("It took {:.2f} seconds for the variable to change".format(duration))
        else:
            self.fail("The value did not change")


if __name__ == "__main__":

    TestWaitFor().run()
