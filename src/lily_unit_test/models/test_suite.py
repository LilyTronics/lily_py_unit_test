"""
Test suite class.
"""

import time
import traceback

from lily_unit_test.models.classification import Classification
from lily_unit_test.models.logger import Logger


class TestSuite(object):
    """
    Base class for all test suites.

    :param report_path: path were the reports are stored.

    The test runner creates the report path and passes it to the test suite. This path can be used in the tests.
    Setting this path here will not change the path where the reports are stored.
    This is determined by the test runner (see test runner class).
    """

    CLASSIFICATION = Classification.PASS

    def __init__(self, report_path=None):
        self._report_path = report_path
        self.log = Logger()

    def run(self, log_traceback=False):
        """
        Run the test suite.

        :param log_traceback: if True, detailed traceback information is written to the logger in case of an exception.
        :return: True when all tests are passed, False when one or more tests are failed.

        The run method creates a list of all methods starting with :code:`test_`. Before executing the test methods,
        it executes the setup method. After executing the test methods, it executes the teardown.
        """
        test_suite_name = self.__class__.__name__
        self.log.info("Run test suite: {}".format(test_suite_name))

        test_suite_result = False
        try:
            test_methods = list(filter(lambda x: x.startswith("test_"), list(vars(self.__class__).keys())))
            n_tests = len(test_methods)
            assert n_tests > 0, "No tests defined (methods starting with 'test_)"

            # Run the setup
            try:
                setup_result = self.setup()
                if setup_result is not None and not setup_result:
                    self.log.error("Test suite {}: FAILED: setup failed".format(test_suite_name))
                    setup_result = False
                else:
                    setup_result = True
            except Exception as e:
                self.log.error("Test suite {}: FAILED by exception in setup\nException: {}".format(test_suite_name, e))
                if log_traceback:
                    self.log.error(traceback.format_exc().strip())
                setup_result = False

            if setup_result:
                n_passed = 0
                # Run the test methods
                for test_method in test_methods:
                    test_case_name = "{}.{}".format(test_suite_name, test_method)
                    self.log.info("Run test case: {}".format(test_case_name))
                    try:
                        method_result = getattr(self, test_method)()
                        if method_result is None or method_result:
                            n_passed += 1
                            self.log.info("Test case {}: PASSED".format(test_case_name))
                        else:
                            self.log.error("Test case {}: FAILED".format(test_case_name))

                    except Exception as e:
                        self.log.error("Test case {}: FAILED by exception\nException: {}".format(test_case_name, e))
                        if log_traceback:
                            self.log.error(traceback.format_exc().strip())

                ratio = 100 * n_passed / n_tests
                self.log.info("Test suite {}: {} of {} test cases passed ({:.1f}%)".format(
                              test_suite_name, n_passed, n_tests, ratio))

                test_suite_result = n_passed == n_tests

            # Run the teardown
            try:
                self.teardown()
            except Exception as e:
                self.log.error("Test suite {}: FAILED by exception in teardown\nException: {}".format(
                               test_suite_name, e))
                test_suite_result = False

        except Exception as e:
            self.log.error("Test suite {}: FAILED by exception\nException: {}".format(test_suite_name, e))
            if log_traceback:
                self.log.error(traceback.format_exc().strip())
            test_suite_result = False

        if self.CLASSIFICATION == Classification.FAIL:
            # We expect a failure
            test_suite_result = not test_suite_result
            if test_suite_result:
                self.log.info("Test suite failed, but accepted because classification is set to 'FAIL'")
            else:
                self.log.error("Test suite passed, but a failure was expected because classification is set to 'FAIL'")
        elif self.CLASSIFICATION != Classification.PASS:
            self.log.error("Test classification is not defined: '{}'".format(self.CLASSIFICATION))
            test_suite_result = False

        if test_suite_result:
            self.log.info("Test suite {}: PASSED".format(test_suite_name))
        else:
            self.log.error("Test suite {}: FAILED".format(test_suite_name))

        self.log.shutdown()

        return test_suite_result

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
        The setup method. This can be overridden in the test suite. This will be executed before running all test
        methods.

        :return: True or None when the setup is passed, False when the setup is failed.

        The test methods are executed after the setup is executed successfully.
        If the setup fails because of either an exception or returning False, the test methods are not executed.
        """
        return True

    def teardown(self):
        """
        The teardown method. This can be overridden in the test suite. This will be executed after running all test
        methods.

        This method is always executed and if there is an exception raise in this method, the test suite is reported
        as failed.
        """
        pass

    ################
    # Test methods #
    ################

    def fail(self, error_message, raise_exception=True):
        """
        Make the test suite fail.

        :param error_message: the error message that should be written to the logger.
        :param raise_exception: if True, an exception is raised and the test suit will stop.
        :return: False
        """
        self.log.error(error_message)
        if raise_exception:
            raise Exception(error_message)
        return False

    def fail_if(self, expression, error_message, raise_exception=True):
        """
        Fail if the given expression evaluates to True.

        :param expression: the expression that should be evaluated.
        :param error_message: the error message that should be written to the logger.
        :param raise_exception: if True, an exception is raised and the test suit will stop.
        :return: False in case of a failure
        """
        if expression:
            self.fail(error_message, raise_exception)

        return not expression

    @staticmethod
    def sleep(sleep_time):
        """
        Simple wrapper for time.sleep()

        :param sleep_time: time to sleep in seconds (can be float)
        """
        time.sleep(sleep_time)


if __name__ == "__main__":

    import os
    import test_suites

    from lily_unit_test.models.test_runner import TestRunner

    TestRunner.run(os.path.dirname(test_suites.__file__))
