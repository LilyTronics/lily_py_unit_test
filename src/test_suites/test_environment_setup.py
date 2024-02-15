"""
Setup the test environment
"""

import os
import shutil
import lily_unit_test


class TestEnvironmentSetup(lily_unit_test.TestSuite):

    def test_setup_environment(self):
        result = True
        report_path = self.get_report_path()
        if report_path is not None:
            self.log.info(f"Remove old log files in {report_path}")
            for item in os.listdir(report_path):
                full_path = os.path.join(report_path, item)
                if os.path.isfile(full_path):
                    # Do not delete release reports
                    if not (item.endswith(".html") and "_latest" in item):
                        self.log.debug(f"Remove file: {full_path}")
                        os.remove(full_path)
                elif os.path.isdir(full_path):
                    self.log.debug(f"Remove folder: {full_path}")
                    shutil.rmtree(full_path)
                else:
                    self.log.error(f"The path '{full_path}' is neither a file or a folder")
                    result = False

        return result


if __name__ == "__main__":

    test_report_path = os.path.abspath(os.path.join("../../",
                                                    lily_unit_test.TestSettings.REPORT_FOLDER_NAME))

    TestEnvironmentSetup(test_report_path).run()
