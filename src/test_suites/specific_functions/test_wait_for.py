"""
Test the wait for API.
"""

import time
import lily_unit_test


class TestWaitFor(lily_unit_test.TestSuite):
    """ Test the wait_for method of the test suite. """

    _test_value = [False]

    def _change_value(self):
        self.sleep(0.5)
        self._test_value[0] = True

    def _update_value(self):
        self._test_value += 1
        return self._test_value

    def test_wait_for_variable(self):
        """ Test waiting for variable change. """
        # Set initial value of the variable
        self._test_value[0] = False
        # We use a thread to manipulate the value independent of the wait for
        self.start_thread(self._change_value)
        start = time.perf_counter()
        result = self.wait_for(self._test_value, True, 1, 0.1)
        if result:
            duration = time.perf_counter() - start
            self.log.debug(f"It took {duration:.2f} seconds for the variable to change")
        else:
            self.fail("The value did not change")

    def test_wait_for_function(self):
        """ Test wait for return value of function change. """
        # Set initial value of the variable
        self._test_value = 0
        start = time.perf_counter()
        result = self.wait_for(self._update_value, 5, 1, 0.1)
        if result:
            duration = time.perf_counter() - start
            self.log.debug(f"It took {duration:.2f} seconds for the variable to change")
        else:
            self.fail("The value did not change")


if __name__ == "__main__":

    TestWaitFor().run()
