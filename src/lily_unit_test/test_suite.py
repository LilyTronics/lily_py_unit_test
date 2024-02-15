"""
Test suite class.
"""

import threading
import time
import traceback

from lily_unit_test.classification import Classification
from lily_unit_test.logger import Logger


class TestSuite:
    """
    Base class for all test suites.

    :param report_path: path were the reports are stored.

    The test runner creates the report path and passes it to the test suite. This path can be used
    in the tests. Setting this path here will not change the path where the reports are stored.
    This is determined by the test runner (see test runner class).
    """

    CLASSIFICATION = Classification.PASS

    def __init__(self, report_path=None):
        self._test_suite_name = self.__class__.__name__
        self._report_path = report_path
        self.log = Logger()
        self._test_suite_result = None
        self._lock = threading.RLock()

    def _set_result(self, result):
        with self._lock:
            self._test_suite_result = result

    def _get_result(self):
        with self._lock:
            result = self._test_suite_result
        return result

    def _get_test_methods(self):
        test_methods = list(filter(lambda x: x.startswith("test_"),
                                   list(vars(self.__class__).keys())))
        n_tests = len(test_methods)
        assert n_tests > 0, "No tests defined (methods starting with 'test_)"
        return test_methods

    def _run_setup(self, log_traceback):
        try:
            setup_result = self.setup()
            if setup_result is not None and not setup_result:
                self.log.error(f"Test suite {self._test_suite_name}: FAILED: setup failed")
                self._set_result(False)
        except Exception as e:
            self.log.error(f"Test suite {self._test_suite_name}: FAILED by exception in setup\n"
                           f"Exception: {e}")
            if log_traceback:
                self.log.error(traceback.format_exc().strip())
            self._set_result(False)

    def _run_test_methods(self, test_methods, log_traceback):
        n_passed = 0
        for test_method in test_methods:
            test_case_name = f"{self._test_suite_name}.{test_method}"
            self.log.info(f"Run test case: {test_case_name}")
            try:
                # Start result None. Test case can set the result to False by using a fail method.
                self._set_result(None)
                method_result = getattr(self, test_method)()
                if (not self.log.has_stderr_messages() and self._get_result() is None and
                        method_result is None or method_result):
                    n_passed += 1
                    self.log.info(f"Test case {test_case_name}: PASSED")
                else:
                    self.log.error(f"Test case {test_case_name}: FAILED")
            except Exception as e:
                self.log.error(f"Test case {test_case_name}: FAILED by exception\nException: {e}")
                if log_traceback:
                    self.log.error(traceback.format_exc().strip())

        ratio = 100 * n_passed / len(test_methods)
        self.log.info(f"Test suite {self._test_suite_name}: "
                      f"{n_passed} of {len(test_methods)} test cases passed ({ratio:.1f}%)")
        self._set_result(n_passed == len(test_methods))

    def _run_teardown(self, log_traceback):
        try:
            self.teardown()
        except Exception as e:
            self.log.error(f"Test suite {self._test_suite_name}: FAILED by exception in teardown\n"
                           f"Exception: {e}")
            if log_traceback:
                self.log.error(traceback.format_exc().strip())
            self._set_result(False)

    def run(self, log_traceback=False):
        """
        Run the test suite.

        :param log_traceback: if True, detailed traceback information is written to the logger in
            case of an exception.
        :return: True when all tests are passed, False when one or more tests are failed.

        The run method creates a list of all methods starting with :code:`test_`.
        Before executing the test methods, it executes the setup method. After executing the test
        methods, it executes the teardown method.
        """
        self.log.info(f"Run test suite: {self._test_suite_name}")

        self._set_result(None)
        try:
            test_methods = self._get_test_methods()
            self._run_setup(log_traceback)
            # After setup, result is either None or False
            if self._get_result() is None:
                self._run_test_methods(test_methods, log_traceback)
            assert self._get_result() is not None, "Unexpected test result None"
            self._run_teardown(log_traceback)
        except Exception as e:
            self.log.error(f"Test suite {self._test_suite_name}: FAILED by exception\n"
                           f"Exception: {e}")
            if log_traceback:
                self.log.error(traceback.format_exc().strip())
            self._set_result(False)

        if self.CLASSIFICATION == Classification.FAIL:
            # We expect a failure
            self._set_result(not self._get_result())
            if self._get_result():
                self.log.info("Test suite failed, "
                              "but accepted because classification is set to 'FAIL'")
            else:
                self.log.error("Test suite passed, "
                               "but a failure was expected because classification is set to 'FAIL'")
        elif self.CLASSIFICATION != Classification.PASS:
            self.log.error(f"Test classification is not defined: '{self.CLASSIFICATION}'")
            self._set_result(False)

        if self._get_result():
            self.log.info(f"Test suite {self._test_suite_name}: PASSED")
        else:
            self.log.error(f"Test suite {self._test_suite_name}: FAILED")

        self.log.shutdown()

        return self._get_result()

    def get_report_path(self):
        """
        Get the path to the report files as set by the test runner.

        :return: string containing the path to the report files.
        """
        return self._report_path

    ##############################
    # Override these when needed #
    ##############################

    def setup(self):
        """
        The setup method. This can be overridden in the test suite. This will be executed before
        running all test methods.

        :return: True or None when the setup is passed, False when the setup is failed.

        The test methods are executed after the setup is executed successfully.
        If the setup fails because of either an exception or returning False, the test methods
        are not executed.
        """
        return True

    def teardown(self):
        """
        The teardown method. This can be overridden in the test suite. This will be executed
        after running all test methods.

        This method is always executed and if there is an exception raised in this method,
        the test suite is reported as failed.
        """

    ################
    # Test methods #
    ################

    def fail(self, error_message, raise_exception=True):
        """
        Make the test suite fail.

        :param error_message: the error message that should be written to the logger.
        :param raise_exception: if True, an exception is raised and the test suite will stop.

        The fail method logs an error message and raises an exception.
        When the exception is raised, the test suite stops and is reported as failed.
        Setting the :code:`raise_exception` to False, does not raise an exception and the test
        suite continues. Even though the test suite continues it is reported as failed.

        .. code-block:: python

            import lily_unit_test

            class MyTestSuite(lily_unit_test.TestSuite):

                def test_something(self):

                    # do some things

                    # In case something is wrong, and we cannot continue.
                    if not check_something_that_must_be_good():
                        # Log a failure with exception, this will make the test suite fail and stop.
                        self.fail("Something is wrong, and we cannot continue")

                    # In case something is wrong, and we still can continue.
                    if not check_if_something_is_ok():
                        # Log a failure without exception, this will make the test suite fail.
                        self.fail("Something is not OK, but we continue", False)

                    # do some other stuff

        """
        self.log.error(error_message)
        if raise_exception:
            raise Exception(error_message)
        self._set_result(False)

    def fail_if(self, expression, error_message, raise_exception=True):
        """
        Fail if the given expression evaluates to True.

        :param expression: the expression that should be evaluated.
        :param error_message: the error message that should be written to the logger.
        :param raise_exception: if True, an exception is raised and the test suite will stop.

        Same as :code:`fail()` but evaluates an expression first.
        If the expression evaluates to :code:`True`, the :code:`fail()` method is executed
        with the given parameters.

        .. code-block:: python

            class MyTestSuite(lily_unit_test.TestSuite):

                def test_something(self):

                    # do some things

                    self.fail_if(not check_something_that_must_be_good(),
                                 "Something is wrong, and we cannot continue")

                    self.fail_if(not check_if_something_is_ok(),
                                 "Something is not OK, but we continue", False)

                    # do some other stuff

        """
        if expression:
            self.fail(error_message, raise_exception)

    @staticmethod
    def sleep(sleep_time):
        """
        Simple wrapper for time.sleep()

        :param sleep_time: time to sleep in seconds (can be fractional)
        """
        time.sleep(sleep_time)

    @staticmethod
    def start_thread(target, args=()):
        """
        Starts a function (target) in a separate thread with the given arguments.

        :param target: function to start as a thread
        :param args: tuple with arguments to pass to the thread
        :return: a reference to the started thread

        The thread is started as a daemon thread, meaning that the thread will be terminated
        when test execution stops.
        The thread can be monitored by the is_alive() method of the thread.

        .. code-block:: python

            import lily_unit_test

            class MyTestSuite(liy_unit_test.TestSuite):

                def back_ground_job(self, some_parameter):
                    # do some time-consuming stuff in the background

                def test_something(self):
                    # Start our background job
                    t = self.start_thread(self.back_ground_job, (parameter_value, ))

                    # do some other stuff while the job is running

                    # Check if our job is running
                    if t.is_alive():
                        self.log.debug("The job is still running")

                    # Wait for the job to finish, with timeout of 30 seconds, check every second.
                    if self.wait_for(t.is_alive, False, 30, 1):
                        self.log.debug("The job is done")
                    else:
                        self.fail("The thread did not finish within 30 seconds.")

                    # Check result from the thread


        Note that if an exception is raised in the thread, the thread is ended.
        The test suite will report a failure.

        Note that the thread may be hanging for some reason and does not stop.
        When checking if the thread is finished,
        a timeout should be included.
        """
        t = threading.Thread(target=target, args=args)
        t.daemon = True
        t.start()
        return t

    @staticmethod
    def wait_for(object_to_check, expected_result, timeout, interval):
        """
        Wait for a certain result with a certain timeout

        :param object_to_check: object must be a list with one element or a function.
                                In case of a function the function is called in every iteration.
        :param expected_result: the expected value for the object to check.
        :param timeout: how long to check (float in seconds).
        :param interval: at what interval to check (float in seconds).
        :return: True when the expected result is met, False when the timer times out.

        This function only works with mutable variables or objects that can be called.
        It does not work on immutable variables since they are not passed as reference.

        .. code-block:: python

            import lily_unit_test

            class MyTestSuite(lily_unit_test.TestSuite):

                def test_wait_for_variable(self):
                    # Set initial value of the variable, put in a list, so it is mutable
                    self._test_value[0] = False

                    # Wait for the variable to change. Wait for automatically checks the first
                    # element of the list
                    result = self.wait_for(self._test_value, True, 1, 0.1)

                def test_wait_for_function(self):
                    # Check the outcome of a function, e.g.: checking if a server is connected.
                    # Note the missing '()' for the function, we pass a reference of the function.
                    result = self.wait_for(server.is_connected, True, 5, 0.1)

        """
        result = None
        while timeout > 0:
            if callable(object_to_check):
                result = object_to_check()
            elif isinstance(object_to_check, list) and len(object_to_check) > 0:
                result = object_to_check[0]
            if result == expected_result:
                return True
            time.sleep(interval)
            timeout -= interval
        return False


if __name__ == "__main__":

    from src.run_tests import run_unit_tests

    run_unit_tests()
