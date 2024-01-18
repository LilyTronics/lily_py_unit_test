"""
Setup the test environment
"""

import os

import lily_unit_test
import shutil


class TestEnvironmentSetup(lily_unit_test.TestSuite):

    def test_setup_environment(self):
        result = True

        report_path = self.get_report_path()
        if report_path is not None:
            self.log.info("Remove old log files in {}".format(report_path))
            for item in os.listdir(report_path):
                full_path = os.path.join(report_path, item)
                if os.path.isfile(full_path):
                    self.log.debug("Remove file: {}".format(full_path))
                    os.remove(full_path)
                elif os.path.isdir(full_path):
                    self.log.debug("Remove folder: {}".format(full_path))
                    shutil.rmtree(full_path)
                else:
                    self.log.error("The path '{}' is neither a file or a folder".format(full_path))
                    result = False

        return result


if __name__ == "__main__":

    test_report_path = os.path.join(os.path.dirname(lily_unit_test.__file__),
                                    lily_unit_test.TestSettings.REPORT_FOLDER_NAME)

    TestEnvironmentSetup(test_report_path).run()
