"""
Cleanup the test environment.
"""

import lily_unit_test


class TestEnvironmentCleanup(lily_unit_test.TestSuite):

    def test_setup_cleanup(self):
        self.log.info("Clean up test environment, nothing to cleanup for now...")


if __name__ == "__main__":

    TestEnvironmentCleanup().run()
