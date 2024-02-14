"""
Lily unit test package
"""

# Disable message for self-assigning-variable in this file
# pylint: disable-msg=W0127

from lily_unit_test.classification import Classification
from lily_unit_test.logger import Logger
from lily_unit_test.test_settings import TestSettings
from lily_unit_test.test_runner import TestRunner
from lily_unit_test.test_suite import TestSuite

# For easy import:
Classification = Classification
Logger = Logger
TestSettings = TestSettings
TestRunner = TestRunner
TestSuite = TestSuite
