"""
Generate HTML report.
"""

import os

from datetime import datetime
from string import Template
from lily_unit_test.models.logger import Logger


def generate_html_report(report_data):
    time_format = Logger.TIME_STAMP_FORMAT.split('.')[0]

    test_runner_start_message = ''
    test_runner_start = ''
    test_runner_end = ''
    test_runner_result = ''
    test_runner_result_message = ''
    test_suites_results = ''

    for key in report_data.keys():
        # Test runner result
        if '1_TestRunner' in key:
            # First message for start time and message
            parts = report_data[key][0].split('|')
            test_runner_start = parts[0].split('.')[0]
            test_runner_start_message = parts[-1].strip()

            # Second last message for result message
            test_runner_result_message = report_data[key][-2].split('|')[-1].strip()

            # Last message for end time and result
            test_runner_end = report_data[key][-1].split('|')[0].split('.')[0]
            if 'PASSED' in report_data[key][-1]:
                test_runner_result = 'PASSED'
            else:
                test_runner_result = 'FAILED'

        else:
            # Test suite results
            test_suites_results += '{}'.format(_generate_test_suite_results(key, report_data[key]))

    start = datetime.strptime(test_runner_start, time_format)
    end = datetime.strptime(test_runner_end, time_format)
    test_runner_duration = end - start

    template_filename = os.path.join(os.path.dirname(__file__), 'artifacts', 'html_report_template.html')
    with open(template_filename, 'r') as fp:
        template = fp.read()

    output = Template(template).substitute({
        'start_message': test_runner_start_message,
        'start_date': test_runner_start,
        'end_date': test_runner_end,
        'duration': test_runner_duration,
        'result': test_runner_result,
        'result_class': test_runner_result.lower(),
        'result_message': test_runner_result_message,
        'test_suites_results': test_suites_results
    })
    return output


def _generate_test_suite_results(test_suite_key, log_messages):
    time_format = Logger.TIME_STAMP_FORMAT.split('.')[0]

    test_name = test_suite_key.split('_')[-1]
    test_start = log_messages[0].split('|')[0].split('.')[0]
    test_end = log_messages[-1].split('|')[0].split('.')[0]
    if 'PASSED' in log_messages[-1]:
        test_result = 'PASSED'
    else:
        test_result = 'FAILED'

    start = datetime.strptime(test_start, time_format)
    end = datetime.strptime(test_end, time_format)
    duration = end - start

    output = '<div class ="test-suite {}">'.format(test_result.lower())
    output += '<span class="expand" title="Show/hide log messages" '
    output += 'id="button_{0}" onclick="show_log(\'{0}\')">&plus;</span> '.format(test_suite_key)
    output += '{}: {} ({})</div>\n'.format(test_name, test_result, duration)
    output += '<div class="log-messages" style="display:none" id="log_{}">\n'.format(test_suite_key)
    for log_message in log_messages:
        level = 'debug'
        parts = log_message.split('|')
        if len(parts) > 1:
            level = parts[1].strip().lower()
        if log_message.strip() == '':
            log_message = '&nbsp;'
        output += '<div class="log {}"><pre>{}</pre></div>\n'.format(level, log_message)
    output += '</div>\n'

    return output.strip()


if __name__ == '__main__':

    import time

    # Generate some report data
    dummy_report_data = {}

    # Test runner log messages
    tr_logger = Logger(log_to_stdout=False)
    tr_logger.info('Run 2 test suites from folder: C:\\path\\to\\test_suites')
    tr_logger.empty_line()
    tr_logger.info('Run test suite: TestCreateHtmlReport')

    # TestCreateHtmlReport log messages
    test_logger = Logger(log_to_stdout=False)
    test_logger.info('Run test suite: TestCreateHtmlReport')
    test_logger.info('Run test case: TestCreateHtmlReport.test_01_log_message_types')
    test_logger.debug('This is a debug message')
    test_logger.error('This is an error message')
    test_logger.debug('The next line is empty')
    test_logger.empty_line()
    test_logger.debug('This line contains HTML entities: > < " \' &. These must be escaped properly.')
    test_logger.handle_message(test_logger.TYPE_STDOUT, 'This is a stdout message\n')
    test_logger.handle_message(test_logger.TYPE_STDERR, 'This is a stderr message\n')
    test_logger.info('Test case TestCreateHtmlReport.test_01_log_message_types: PASSED')
    time.sleep(1.2)
    test_logger.info('Test suite TestPublishHtmlReport: 1 of 1 test cases passed (100.0%)')
    test_logger.info('Test suite TestCreateHtmlReport: PASSED')
    test_logger.shutdown()
    dummy_report_data['2_TestCreateHtmlReport'] = test_logger.get_log_messages()

    tr_logger.error('Test suite: TestCreateHtmlReport PASSED')
    tr_logger.empty_line()
    tr_logger.info('Run test suite: TestPublishHtmlReport')

    # TestPublishHtmlReport log messages
    test_logger = Logger(log_to_stdout=False)
    test_logger.info('Run test suite: TestPublishHtmlReport')
    test_logger.info('Run test case: TestPublishHtmlReport.test_01_upload_to_ftp')
    test_logger.error('Test case: TestPublishHtmlReport.test_01_upload_to_ftp: FAILED by exception')
    test_logger.error('Exception: connection refused by host,invalid authorisation')
    time.sleep(1.2)
    test_logger.info('Test suite TestPublishHtmlReport: 0 of 1 test cases passed (0.0%)')
    test_logger.error('Test suite TestClassFail: FAILED')
    test_logger.shutdown()
    dummy_report_data['3_TestPublishHtmlReport'] = test_logger.get_log_messages()

    tr_logger.info('Test suite: TestPublishHtmlReport FAILED')
    tr_logger.empty_line()
    tr_logger.info('1 of 2 test suites passed (50.0%)')
    tr_logger.error('Test runner result: FAILED')
    tr_logger.shutdown()
    dummy_report_data['1_TestRunner'] = tr_logger.get_log_messages()

    with open('test_report.html', 'w') as fp_out:
        fp_out.write(generate_html_report(dummy_report_data))
