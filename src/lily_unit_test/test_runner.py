"""
Test runner class.
Runs all test suites from a specific package folder (recursive)
"""
# pylint: disable=too-few-public-methods

import inspect
import os
import sys
import webbrowser

from datetime import datetime
from lily_unit_test.html_report import generate_html_report
from lily_unit_test.logger import Logger
from lily_unit_test.test_settings import TestSettings
from lily_unit_test.test_suite import TestSuite


class TestRunner:
    """
    Static class that runs test suites in a specified folder.
    """

    ###########
    # Private #
    ###########

    @classmethod
    def _parse_options(cls, options, test_suites_path):
        parsed_options = {
            "report_folder": os.path.join(os.path.dirname(test_suites_path),
                                          TestSettings.REPORT_FOLDER_NAME),
            "create_html_report": False,
            "open_in_browser": False,
            "no_log_files": False,
            "include_test_suites": [],
            "exclude_test_suites": [],
            "run_first": None,
            "run_last": None
        }
        if options is not None:
            for key in options:
                parsed_options[key] = options[key]

        return parsed_options

    @classmethod
    def _populate_test_suites(cls, options):
        sys.path.append(options["test_suites_path"])

        found_test_suites = []
        for current_folder, sub_folders, filenames in os.walk(options["test_suites_path"]):
            sub_folders.sort()
            filenames.sort()
            for filename in filter(lambda x: x.endswith(".py"), filenames):
                import_path = os.path.join(current_folder[len(options["test_suites_path"]) + 1:],
                                           filename.replace(".py", ""))
                import_path = import_path.replace(os.sep, ".")
                module = __import__(str(import_path), fromlist=["*"])
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if inspect.isclass(attribute):
                        classes = inspect.getmro(attribute)
                        if len(classes) > 2 and TestSuite in classes:
                            found_test_suites.append(attribute)

        return cls._filter_test_suites(found_test_suites, options)

    @classmethod
    def _filter_test_suites(cls, found_test_suites, options):
        if len(options["include_test_suites"]) > 0:
            found_test_suites = list(filter(lambda x: x.__name__ in options["include_test_suites"],
                                            found_test_suites))

        if len(options["exclude_test_suites"]) > 0:
            found_test_suites = list(filter(lambda x: x.__name__ not in
                                            options["exclude_test_suites"],
                                            found_test_suites))

        run_first = options["run_first"]
        run_last = options["run_last"]
        if run_first is not None and options["run_first"] != "":
            matches = list(filter(lambda x: x.__name__ == run_first, found_test_suites))
            assert len(matches) == 1, f"Test suite to run first with name '{run_first}' not found"
            found_test_suites.remove(matches[0])
            found_test_suites.insert(0, matches[0])

        if run_last is not None and run_last != "":
            matches = list(filter(lambda x: x.__name__ == run_last, found_test_suites))
            assert len(matches) == 1, f"Test suite to run last with name '{run_last}' not found"
            found_test_suites.remove(matches[0])
            found_test_suites.append(matches[0])

        return found_test_suites

    @classmethod
    def _write_log_messages_to_file(cls, report_path, time_stamp, filename, logger):
        output_path = os.path.join(report_path, time_stamp)
        if not os.path.isdir(output_path):
            os.makedirs(output_path)

        with open(os.path.join(str(output_path), filename), "w", encoding="utf-8") as fp:
            fp.writelines(map(lambda x: f"{x}\n", logger.get_log_messages()))

    @classmethod
    def _run_test_suites(cls, test_suites_to_run, report_data, time_stamp, options):
        n_test_suites_passed = 0
        report_name_format = f"{{:0{len(str(len(test_suites_to_run)))}d}}_{{}}"
        logger = Logger(False)
        if len(test_suites_to_run) > 0:
            logger.info(f"Run {len(test_suites_to_run)} test suites from folder: "
                        f"{options["test_suites_path"]}")
            for i, test_suite in enumerate(test_suites_to_run):
                ts = test_suite(options["report_folder"])
                n_test_suites_passed += cls._run_test_suite(ts, logger)
                report_id = report_name_format.format(i + 2, test_suite.__name__)
                report_data[report_id] = ts.log.get_log_messages()
                if not options["no_log_files"]:
                    cls._write_log_messages_to_file(options["report_folder"], time_stamp,
                                                    f"{report_id}.txt", ts.log)
        else:
            logger.info(f"No test suites found in folder: {options["test_suites_path"]}")

        logger.empty_line()

        ratio = 100 * n_test_suites_passed / len(test_suites_to_run)
        logger.info(f"{n_test_suites_passed} of {len(test_suites_to_run)} "
                    f"test suites passed ({ratio:.1f}%)")
        if len(test_suites_to_run) == n_test_suites_passed:
            logger.info("Test runner result: PASSED")
        else:
            logger.error("Test runner result: FAILED")

        report_id = report_name_format.format(1, "TestRunner")
        report_data[report_id] = logger.get_log_messages()
        if not options["no_log_files"]:
            cls._write_log_messages_to_file(options["report_folder"], time_stamp,
                                            f"{report_id}.txt", logger)
        logger.shutdown()

        return len(test_suites_to_run) == n_test_suites_passed

    @classmethod
    def _run_test_suite(cls, test_suite, logger):
        result_count = 0
        test_suite_name = test_suite.__class__.__name__
        logger.empty_line()
        logger.log_to_stdout(False)
        logger.info(f"Run test suite: {test_suite_name}")
        logger.log_to_stdout(True)
        result = test_suite.run()
        result_text = "FAILED"
        log_method = logger.error
        if result is None or result:
            result_count = 1
            result_text = "PASSED"
            log_method = logger.info

        logger.log_to_stdout(False)
        log_method(f"Test suite {test_suite_name}: {result_text}")
        logger.log_to_stdout(True)

        return result_count

    ##########
    # Public #
    ##########

    @classmethod
    def run(cls, test_suites_path, options=None):
        """
        Run the test suites that are found in the given path recursively.

        :param test_suites_path: path to the test suites
        :param options: a dictionary with options, if no dictionary is given, defaults are used
        :return: True, if all test suites are passed

        Options:
        The options dictionary can have the following values:

        ===================== ========================== ===========================================
        Key name              Default value              Description
        ===================== ========================== ===========================================
        | report_folder       | "lily_unit_test_reports" | The path where the reports are written.
                                                         | The path is by default at the same level
                                                         | as the test_suites_path. When setting
                                                         | a path, use an absolute path.
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
        ===================== ========================== ===========================================

        Not all keys have to present, you can omit keys. For the missing keys, defaults are used.
        For test suite names, use their class names.

        Example: using HTML reporting and skip the text log files:

        .. code-block:: python

            from lily_unit_test import TestRunner

            options = {
                # Creates a single HTML file with all the results
                "create_html_report": True,

                # Open the HTML report in the default browser when finished
                "open_in_browser": True,

                # Do not write log files, because we use the HTML report
                "no_log_files": True
            }
            TestRunner.run(".", options)

        Example: skipping test suites

        .. code-block:: python

            from lily_unit_test import TestRunner, TestSuite

            class MyTestSuite(TestSuite):
                # some test stuff

            # options for the test runner:
            options = {
                "exclude_test_suites": ["MyTestSuite"]
            }
            TestRunner.run(".", options)

        Example: running only one test suite

        .. code-block:: python

            from lily_unit_test import TestRunner, TestSuite

            class MyTestSuite(TestSuite):
                # some test stuff

            # options for the test runner:
            options = {
                "include_test_suites": ["MyTestSuite"]
            }
            TestRunner.run(".", options)

        Example: run specific test suites first and last

        .. code-block:: python

            from lily_unit_test import TestRunner, TestSuite

            class TestEnvironmentSetup(TestSuite):
                # Set up our test environment using test methods

            class TestEnvironmentCleanup(TestSuite):
                # Clean up our test environment using test methods

            options = {
                "run_first": "TestEnvironmentSetup",
                "run_last": "TestEnvironmentCleanup"
            }
            TestRunner.run(".", options)

        Because the options are in a dictionary, they can be easily read from a JSON file.

        .. code-block:: python

            import json
            from lily_unit_test import TestRunner

            TestRunner.run(".", json.load(open("/path/to/json_file", "r")))

        This makes it easy to automate tests using different configurations.
        """
        test_suites_path = os.path.abspath(test_suites_path)
        options = cls._parse_options(options, test_suites_path)
        options["test_suites_path"] = test_suites_path
        test_suites_to_run = cls._populate_test_suites(options)
        time_stamp = datetime.now().strftime(TestSettings.REPORT_TIME_STAMP_FORMAT)

        report_data = {}
        test_run_result = cls._run_test_suites(test_suites_to_run, report_data, time_stamp, options)

        if options.get("create_html_report", False):
            html_output = generate_html_report(report_data)
            filename = os.path.join(options["report_folder"], f"{time_stamp}_TestRunner.html")
            if not os.path.isdir(options["report_folder"]):
                os.makedirs(options["report_folder"])
            with open(filename, "w", encoding="utf-8") as fp:
                fp.write(html_output)

            if options.get("open_in_browser", False):
                webbrowser.open(filename)

        return test_run_result


if __name__ == "__main__":

    from src.run_tests import run_unit_tests

    run_unit_tests()
