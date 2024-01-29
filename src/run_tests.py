"""
Run all the unit tests.
"""

from lily_unit_test import TestRunner

options = {
    "create_html_report": True,
    "no_log_files": True,
    "open_in_browser": True,
    "run_first": "TestEnvironmentSetup",
    "run_last": "TestEnvironmentCleanup"
}

TestRunner.run(".", options)
