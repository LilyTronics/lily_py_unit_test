"""
Test runner class.
Runs all test suites from a specific package folder (recursive)
"""

import inspect
import os
import sys
import webbrowser

from datetime import datetime
from lily_unit_test.html_report import generate_html_report
from lily_unit_test.logger import Logger
from lily_unit_test.test_settings import TestSettings
from lily_unit_test.test_suite import TestSuite


class TestRunner(object):
    """
    Static class that runs test suites in a specified folder.
    """

    ###########
    # Private #
    ###########

    @classmethod
    def _populate_test_suites(cls, test_suites_path):
        sys.path.append(test_suites_path)

        test_suites = []
        for current_folder, sub_folders, filenames in os.walk(test_suites_path):
            sub_folders.sort()
            filenames.sort()
            for filename in filter(lambda x: x.endswith(".py"), filenames):
                import_path = os.path.join(current_folder[len(test_suites_path) + 1:], filename.replace(".py", ""))
                import_path = import_path.replace(os.sep, ".")
                module = __import__(str(import_path), fromlist=["*"])
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if inspect.isclass(attribute):
                        classes = inspect.getmro(attribute)
                        if len(classes) > 2 and TestSuite in classes:
                            test_suites.append(attribute)

        return test_suites

    @classmethod
    def _write_log_messages_to_file(cls, report_path, time_stamp, filename, logger):
        output_path = os.path.join(report_path, time_stamp)
        if not os.path.isdir(output_path):
            os.makedirs(output_path)

        with open(os.path.join(str(output_path), filename), "w") as fp:
            fp.writelines(map(lambda x: "{}\n".format(x), logger.get_log_messages()))

    ##########
    # Public #
    ##########

    @classmethod
    def run(cls, test_suites_path, options=None):
        """
        Run the test suites that are found in the given path recursively.

        :param test_suites_path: path to the test suites
        :param options: a dictionary with options, if no dictionary is given, default options are used
        :return: True, if all test suites are passed

        Options:
        The options dictionary can have the following values:

        ===================== ========================== =============================================
        Key name              Default value              Description
        ===================== ========================== =============================================
        | report_folder       | "lily_unit_test_reports" | The path where the reports are written.
                                                         | The path is by default at the same level
                                                         | as the test_suites_path.
                                                         | When defining a path, use an absolute path.
        | create_html_report  | False                    | Create a single file HTML report.
        | open_in_browser     | False                    | Open the HTML report in the default
                                                         | browser when all tests are finished.
        | no_log_files        | False                    | Skip writing text log files.
                                                         | In case another form of logging is used,
                                                         | writing text log files can be skipped.
        | include_test_suites | []                       | Only run the test suites in this list.
                                                         | Other test suites are skipped.
        | exclude_test_suites | []                       | Skip the test suites in this list.
        | run_first           | None                     | Run this test suite first.
        | run_last            | None                     | Run this test suite last.
        ===================== ========================== =============================================

        Not all keys have to present, you can omit keys. For the missing keys, default values are used.

        For test suite names, use their class names:

        .. code-block:: python

            import lily_unit_test

            class MyTestSuite(lily_unit_test.TestSuite):
                ...
                some test stuff
                ...

            # options for the test runner:
            options = {
                "include_test_suites": ["MyTestSuite"]
            }
            # Run the test runner from the current folder with the given options
            lily_unit_test.TestRunner.run(".", options)

        """
        test_run_result = False

        if options is None:
            options = {}

        test_suites_path = os.path.abspath(test_suites_path)

        report_path = options.get(
            "report_folder",
            os.path.join(os.path.dirname(test_suites_path), TestSettings.REPORT_FOLDER_NAME)
        )
        write_log_files = not options.get("no_log_files", False)

        report_data = {}
        test_runner_log = Logger(False)
        time_stamp = datetime.now().strftime(TestSettings.REPORT_TIME_STAMP_FORMAT)

        test_suites = cls._populate_test_suites(test_suites_path)

        include_filter = options.get("include_test_suites", [])
        if len(include_filter) > 0:
            test_suites = list(filter(lambda x: x.__name__ in include_filter, test_suites))

        exclude_filter = options.get("exclude_test_suites", [])
        if len(exclude_filter) > 0:
            test_suites = list(filter(lambda x: x.__name__ not in exclude_filter, test_suites))

        run_first = options.get("run_first", None)
        if run_first is not None and run_first != "":
            matches = list(filter(lambda x: x.__name__ == run_first, test_suites))
            assert len(matches) == 1, "Test suite to run first with name '{}' not found".format(run_first)
            test_suites.remove(matches[0])
            test_suites.insert(0, matches[0])

        run_last = options.get("run_last", None)
        if run_last is not None and run_last != "":
            matches = list(filter(lambda x: x.__name__ == run_last, test_suites))
            assert len(matches) == 1, "Test suite to run last with name '{}' not found".format(run_last)
            test_suites.remove(matches[0])
            test_suites.append(matches[0])

        n_test_suites = len(test_suites)
        n_digits = len(str(n_test_suites))
        report_name_format = "{{:0{}d}}_{{}}".format(n_digits)
        if n_test_suites > 0:
            n_test_suites_passed = 0
            test_runner_log.info("Run {} test suites from folder: {}".format(n_test_suites, test_suites_path))

            for i, test_suite in enumerate(test_suites):
                test_suite_name = test_suite.__name__
                test_runner_log.empty_line()
                ts = test_suite(report_path)
                result = ts.run()
                if result is None or result:
                    n_test_suites_passed += 1

                report_id = report_name_format.format(i + 2, test_suite_name)
                report_data[report_id] = ts.log.get_log_messages()
                if write_log_files:
                    cls._write_log_messages_to_file(report_path, time_stamp, "{}.txt".format(report_id), ts.log)

            test_runner_log.empty_line()
            ratio = 100 * n_test_suites_passed / n_test_suites
            test_runner_log.info("{} of {} test suites passed ({:.1f}%)".format(
                                 n_test_suites_passed, n_test_suites, ratio))
            if n_test_suites == n_test_suites_passed:
                test_runner_log.info("Test runner result: PASSED")
                test_run_result = True
            else:
                test_runner_log.error("Test runner result: FAILED")

        else:
            test_runner_log.info("No test suites found in folder: {}".format(test_suites_path))

        test_runner_log.shutdown()

        report_id = report_name_format.format(1, "TestRunner")
        report_data[report_id] = test_runner_log.get_log_messages()
        if write_log_files:
            cls._write_log_messages_to_file(report_path, time_stamp, "{}.txt".format(report_id), test_runner_log)

        if options.get("create_html_report", False):
            html_output = generate_html_report(report_data)
            filename = os.path.join(report_path, "{}_TestRunner.html".format(time_stamp))
            if not os.path.isdir(report_path):
                os.makedirs(report_path)
            with open(filename, "w") as fp:
                fp.write(html_output)

            if options.get("open_in_browser", False):
                webbrowser.open(filename)

        return test_run_result


if __name__ == "__main__":

    import test_suites

    test_options = {
        "create_html_report": True,
        "open_in_browser": True,
        "no_log_files": True,
        "run_first": "TestEnvironmentSetup",
        "run_last": "TestEnvironmentCleanup"
    }

    test_result = TestRunner.run(os.path.dirname(test_suites.__file__), test_options)
    print("Test runner result:", test_result)
