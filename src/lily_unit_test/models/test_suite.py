"""
Test suite class.
"""

import traceback

from lily_unit_test.models.classification import Classification
from lily_unit_test.models.logger import Logger


class TestSuite(object):

    CLASSIFICATION = Classification.PASS

    def __init__(self):
        self.log = Logger()

    def run(self, log_traceback=False):
        test_suite_name = self.__class__.__name__
        self.log.info('Run test suite: {}'.format(test_suite_name))

        test_suite_result = False
        try:
            test_methods = list(filter(lambda x: x.startswith('test_'), list(vars(self.__class__).keys())))
            n_tests = len(test_methods)
            assert n_tests > 0, 'No tests defined'

            # Run the setup
            try:
                setup_result = self.setup()
                if setup_result is not None and not setup_result:
                    self.log.error('Test suite {}: FAILED: setup failed'.format(test_suite_name))
                    setup_result = False
                else:
                    setup_result = True
            except Exception as e:
                self.log.error('Test suite {}: FAILED by exception in setup\nException: {}'.format(test_suite_name, e))
                if log_traceback:
                    self.log.error(traceback.format_exc().strip())
                setup_result = False

            if setup_result:
                n_passed = 0
                # Run the test methods
                for test_method in test_methods:
                    test_case_name = '{}.{}'.format(test_suite_name, test_method)
                    self.log.info('Run test case: {}'.format(test_case_name))
                    try:
                        method_result = getattr(self, test_method)()
                        if method_result is None or method_result:
                            n_passed += 1
                            self.log.info('Test case {}: PASSED'.format(test_case_name))
                        else:
                            self.log.error('Test case {}: FAILED'.format(test_case_name))

                    except Exception as e:
                        self.log.error('Test case {}: FAILED by exception\nException: {}'.format(test_case_name, e))
                        if log_traceback:
                            self.log.error(traceback.format_exc().strip())

                ratio = 100 * n_passed / n_tests
                self.log.info('Test suite {}: {} of {} test cases passed ({:.1f}%)'.format(
                              test_suite_name, n_passed, n_tests, ratio))

                test_suite_result = n_passed == n_tests

            # Run the teardown
            try:
                self.teardown()
            except Exception as e:
                self.log.error('Test suite {}: FAILED by exception in teardown\nException: {}'.format(
                               test_suite_name, e))
                test_suite_result = False

        except Exception as e:
            self.log.error('Test suite {}: FAILED by exception\nException: {}'.format(test_suite_name, e))
            if log_traceback:
                self.log.error(traceback.format_exc().strip())
            test_suite_result = False

        if self.CLASSIFICATION == Classification.FAIL:
            # We expect a failure
            test_suite_result = not test_suite_result
            if test_suite_result:
                self.log.info('Test suite failed, but accepted because classification is set to FAIL')
            else:
                self.log.error('Test suite passed, but a failure was expected because classification is set to FAIL')
        elif self.CLASSIFICATION != Classification.PASS:
            self.log.error('Test classification is not defined: {}'.format(self.CLASSIFICATION))
            test_suite_result = False

        if test_suite_result:
            self.log.info('Test suite {}: PASSED'.format(test_suite_name))
        else:
            self.log.error('Test suite {}: FAILED'.format(test_suite_name))

        self.log.shutdown()

        return test_suite_result

    ##############################
    # Override these when needed #
    ##############################

    def setup(self): return True
    def teardown(self): pass

    ################
    # Test methods #
    ################

    def fail(self, error_message, raise_exception=True):
        self.log.error(error_message)
        if raise_exception:
            raise Exception(error_message)
        return False

    def fail_if(self, expression, error_message, raise_exception=True):
        if expression:
            self.fail(error_message, raise_exception)

        return not expression


if __name__ == '__main__':

    import os

    from lily_unit_test import test_classes
    from lily_unit_test.models.test_runner import TestRunner

    TestRunner.run(os.path.dirname(test_classes.__file__))
