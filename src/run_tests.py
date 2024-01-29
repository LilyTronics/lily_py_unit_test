"""
Run all the unit tests.
"""

import os

from lily_unit_test import TestRunner
from lily_unit_test.test_settings import TestSettings


report_folder = os.path.abspath(os.path.join(os.path.dirname("../"), TestSettings.REPORT_FOLDER_NAME))
if not os.path.isdir(report_folder):
    os.makedirs(report_folder)

options = {
    "report_folder": report_folder,
    "create_html_report": True,
    "no_log_files": True,
    "open_in_browser": True,
    "run_first": "TestEnvironmentSetup",
    "run_last": "TestEnvironmentCleanup"
}

TestRunner.run("./test_suites", options)
