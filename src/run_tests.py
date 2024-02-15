"""
Run all the unit tests.
"""

import os

from lily_unit_test import TestRunner
from lily_unit_test.test_settings import TestSettings


def run_unit_tests():
    root_path = os.path.dirname(__file__)
    report_folder = os.path.join(os.path.dirname(root_path), TestSettings.REPORT_FOLDER_NAME)
    if not os.path.isdir(report_folder):
        os.makedirs(report_folder)

    options = {
        "report_folder": report_folder,
        "create_html_report": True,
        "open_in_browser": True,
        "run_first": "TestEnvironmentSetup",
        "run_last": "TestEnvironmentCleanup"
    }

    TestRunner.run(os.path.join(root_path, "test_suites"), options)


if __name__ == "__main__":

    run_unit_tests()
