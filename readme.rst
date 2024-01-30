Lily unit test package for Python
=================================

This package aims to be a ful alternative to the Python's build in unittest package.
This package has the following features:

- Test suite class with various build-in functions.
- Test runner that scans all Python files in your project for test suites and executes them.
- Single page HTML report: `Test Report V1.8.0 <https://htmlpreview.github.io/?https://github.com/LilyTronics/lily-py-unit-test/blob/main/lily_unit_test_reports/20240130_073058_Test_Report_V1.8.0.html>`_.
- Text log file of every test suit that was executed.

| The source code is available on `GitHub <https://github.com/LilyTronics/lily-py-unit-test>`_.
| The package is available on `PyPi <https://pypi.org/project/lily-unit-test>`_.

Installation
------------

Install the package from PyPi:

.. code-block:: console

   pip install lily-unit-test

Usage
-----

The following example shows a basic test suite for your python code:

.. code-block:: python

    # Import the package
    import lily_unit_test

    # Some functions that needs testing

    def add_one(x):
        return x + 1

    def add_two(x):
        return x + 2


    # Simply make a sub class of the lily unit test test suite
    class MyTestSuite(lily_unit_test.TestSuite):


        def test_add_one(self):
            assert MyClass.add_one(3) == 4, "Wrong return value"


        def test_add_two(self):
            assert MyClass.add_two(3) == 5, "Wrong return value"


    if __name__ == "__main__":

        # Run the test suite
        MyTestSuite().run()

Run the Python file, the output should look like this:

.. code-block:: console

    2023-12-20 19:28:46.105 | INFO   | Run test suite: MyTestSuite
    2023-12-20 19:28:46.105 | INFO   | Run test case: MyTestSuite.test_add_one
    2023-12-20 19:28:46.106 | INFO   | Test case MyTestSuite.test_add_one: PASSED
    2023-12-20 19:28:46.106 | INFO   | Run test case: MyTestSuite.test_add_two
    2023-12-20 19:28:46.106 | INFO   | Test case MyTestSuite.test_add_two: PASSED
    2023-12-20 19:28:46.106 | INFO   | Test suite MyTestSuite: 2 of 2 test cases passed (100.0%)
    2023-12-20 19:28:46.106 | INFO   | Test suite MyTestSuite: PASSED

Run the test runner to run all test suites in a folder:

.. code-block:: python

    from lily_unit_test import TestRunner

    TestRunner.run("path/to/test_suites")

The test runner scans the folder recursively for Python files containing a test suite class.

More detailed information can be found in the `documentation on Read the Docs <https://lily-py-unit-test.readthedocs.io>`_.

.. image:: https://readthedocs.org/projects/lily-py-unit-test/badge/?version=latest
    :target: https://lily-py-unit-test.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Created and owned by `LilyTronics <https://lilytronics.nl>`_
