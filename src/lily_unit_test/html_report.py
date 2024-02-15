"""
Generate HTML report.
"""

import html
import os

from datetime import datetime
from string import Template
from lily_unit_test.logger import Logger


def generate_html_report(report_data):
    time_format = Logger.TIME_STAMP_FORMAT.split(".", maxsplit=1)[0]

    template_values = {
        "start_message": "",
        "start_date": "",
        "end_date": "",
        "duration": "",
        "result": "",
        "result_class": "",
        "result_message": "",
        "test_suites_results": ""
    }

    for key in report_data.keys():
        # Test runner result
        if "1_TestRunner" in key:
            # First message for start time and message
            parts = report_data[key][0].split("|")
            template_values["start_date"] = parts[0].split(".")[0]
            template_values["start_message"] = parts[-1].strip()

            # Second last message for result message
            template_values["result_message"] = report_data[key][-2].split("|")[-1].strip()

            # Last message for end time and result
            template_values["end_date"] = report_data[key][-1].split("|")[0].split(".")[0]
            if "PASSED" in report_data[key][-1]:
                template_values["result"] = "PASSED"
            else:
                template_values["result"] = "FAILED"

        else:
            # Test suite results
            template_values["test_suites_results"] += _generate_test_suite_results(key,
                                                                                   report_data[key])

    start = datetime.strptime(template_values["start_date"], time_format)
    end = datetime.strptime(template_values["end_date"], time_format)
    template_values["duration"] = end - start

    template_filename = os.path.join(os.path.dirname(__file__), "artifacts",
                                     "html_report_template.html")
    with open(template_filename, "r", encoding="utf-8") as fp:
        template = fp.read()

    template_values["result_class"] = template_values["result"].lower()

    output = Template(template).substitute(template_values)
    return output


def _generate_test_suite_results(test_suite_key, log_messages):
    time_format = Logger.TIME_STAMP_FORMAT.split(".", maxsplit=1)[0]

    test_name = test_suite_key.split("_")[-1]
    test_start = log_messages[0].split("|")[0].split(".")[0]
    test_end = log_messages[-1].split("|")[0].split(".")[0]
    if "PASSED" in log_messages[-1]:
        test_result = "PASSED"
    else:
        test_result = "FAILED"

    start = datetime.strptime(test_start, time_format)
    end = datetime.strptime(test_end, time_format)
    duration = end - start

    output = f'<div class="test-suite {test_result.lower()}">'
    output += '<span class="expand" title="Show/hide log messages" '
    output += f'id="button_{test_suite_key}" '
    output += f'onclick="show_log(\'{test_suite_key}\')">&plus;</span> '
    output += f"{test_name}: {test_result} ({duration})</div>\n"
    output += f'<div class="log-messages" style="display:none" id="log_{test_suite_key}">\n'
    for log_message in log_messages:
        level = "debug"
        parts = log_message.split("|")
        if len(parts) > 1:
            level = parts[1].strip().lower()
        if log_message.strip() == "":
            log_message = "&nbsp;"
        else:
            log_message = html.escape(log_message)
        output += f'<div class="log {level}"><pre>{log_message}</pre></div>\n'
    output += "</div>\n"

    return output.strip()


if __name__ == "__main__":

    import time

    # Generate some report data
    dummy_report_data = {}

    # Test runner log messages
    tr_logger = Logger(log_to_stdout=False)
    tr_logger.info("Run 2 test suites from folder: C:\\path\\to\\test_suites")
    tr_logger.empty_line()
    tr_logger.info("Run test suite: TestCreateHtmlReport")

    # TestCreateHtmlReport log messages
    test_logger = Logger(log_to_stdout=False)
    test_logger.info("Run test suite: TestCreateHtmlReport")
    test_logger.info("Run test case: TestCreateHtmlReport.test_01_log_message_types")
    test_logger.debug("This is a debug message")
    test_logger.error("This is an error message")
    test_logger.debug("The next line is empty")
    test_logger.empty_line()
    test_logger.debug('This line contains HTML entities: <div class="error">&nbsp;</div>. '
                      'These must be escaped properly.')
    test_logger.handle_message(test_logger.TYPE_STDOUT, "This is a stdout message\n")
    test_logger.handle_message(test_logger.TYPE_STDERR, "This is a stderr message\n")
    test_logger.info("Test case TestCreateHtmlReport.test_01_log_message_types: PASSED")
    time.sleep(1.2)
    test_logger.info("Test suite TestPublishHtmlReport: 1 of 1 test cases passed (100.0%)")
    test_logger.info("Test suite TestCreateHtmlReport: PASSED")
    test_logger.shutdown()
    dummy_report_data["2_TestCreateHtmlReport"] = test_logger.get_log_messages()

    tr_logger.error("Test suite: TestCreateHtmlReport PASSED")
    tr_logger.empty_line()
    tr_logger.info("Run test suite: TestPublishHtmlReport")

    # TestPublishHtmlReport log messages
    test_logger = Logger(log_to_stdout=False)
    test_logger.info("Run test suite: TestPublishHtmlReport")
    test_logger.info("Run test case: TestPublishHtmlReport.test_01_upload_to_ftp")
    test_logger.error("Test case: TestPublishHtmlReport.test_01_upload_to_ftp: FAILED by exception")
    test_logger.error("Exception: connection refused by host,invalid authorisation")
    time.sleep(1.2)
    test_logger.info("Test suite TestPublishHtmlReport: 0 of 1 test cases passed (0.0%)")
    test_logger.error("Test suite TestClassFail: FAILED")
    test_logger.shutdown()
    dummy_report_data["3_TestPublishHtmlReport"] = test_logger.get_log_messages()

    tr_logger.info("Test suite: TestPublishHtmlReport FAILED")
    tr_logger.empty_line()
    tr_logger.info("1 of 2 test suites passed (50.0%)")
    tr_logger.error("Test runner result: FAILED")
    tr_logger.shutdown()
    dummy_report_data["1_TestRunner"] = tr_logger.get_log_messages()

    with open("test_report.html", "w", encoding="utf-8") as fp_out:
        fp_out.write(generate_html_report(dummy_report_data))
