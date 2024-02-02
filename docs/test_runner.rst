The test runner
===============

The test runner collects and runs a number of test suites and
writes all the results to report files.

Run the test runner
-------------------

Running the test runner is as simple as:

.. code-block:: python

    from lily_unit_test import TestRunner

    TestRunner.run("path/to/test_suites")

The test runner can be configured with a dictionary containing options.
See the test runner API section for all available options and examples.

Collecting and running test suites
----------------------------------

Test suites are recursively collected from the Python files in the given folder.
Given the following project structure:

.. code-block:: console

    project_files
      |- src
      |   |- folder_01
      |   |   |- module_01.py
      |   |   |- module_02.py
      |   |
      |   |- folder_02
      |       |- module_03.py
      |       |- module_04.py
      |
      |- test
          |- test_runner.py

The test_runner.py contains the following code:

.. code-block:: python

    from lily_unit_test import TestRunner

    TestRunner.run("../src")

The test runner is located in the :code:`test` folder.
The test runner will run all tests in the folder: :code:`../src`.
This is relative to the :code:`test` folder. Be sure to run the test runner from the :code:`test` folder.
You can also use an absolute path to the folder containing the test suites.

The test runner will scan all Python modules in the folder :code:`src` recursively.
This means all 4 python modules are checked for test suites.

The test runner imports each module and checks if the module contains a class that is
based on the test suite base class (e.g.: :code:`class MyTestSuite(lily_unit_test.TestSuite)`).

All test suites are executed in alphabetical order.
If a specific order is required, use numbers in the file and folder names to sort them.
The test runner will run all the test suites and will write report files to a folder.
The output folder will look something like this:

.. code-block:: console

    project_files
     |- src
     |- tests
     |- lily_unit_test_reports                  // generic report folder
         |- 20231220_143717                     // date and time of the test run
             |- 1_TestRunner.txt                // test runner log
             |- 2_TestSuiteFromModule01.txt     // test suite log
             |- 3_TestSuiteFromModule02.txt     // test suite log
             |- 4_TestSuiteFromModule03.txt     // test suite log
             |- 5_TestSuiteFromModule04.txt     // test suite log

The first log file is from the test runner. This contains an overview of all test suites that are executed and their
results. For each test suite a specific log file is created, containing all the messages from the test suite logger.

Test Runner API
---------------

.. currentmodule:: lily_unit_test

.. autoclass:: TestRunner
    :members: run
