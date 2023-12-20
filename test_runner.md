# Test runner

The test runner collects and runs a number of test suites and
writes all the results to report files.


## Run the test runner

Running the test runner is a simple as:

    from lily_unit_test import TestRunner

    TestRunner.run('path/to/test_suites')


## Collecting and running test suites

Test suites are recursively collected from the Python files in the given folder.
Given the following project structure:

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
      |- tests
          |- test_runner.py

The test_runner.py contains the following code:
    
    from lily_unit_test import TestRunner

    TestRunner.run('../src')

The test runner is located in the `./tests` folder.
The test runner will run all tests in the folder: `../src`.
This is relative to the `tests` folder. Be sure to run the test runner from the `tests`folder.
You can also use an absolute path to the folder.

The test runner will scan all modules in the folder in `src` recursively.
This means all 4 python modules are checked for test suites.

The test runner imports each module and checks if the module contains a class that
based on the test suite base class (`class MyTestSuite(lily_unit_test.TestSuite)`).

The test runner will run all the test suites and will write report files to a folder:
The output folder will look like this:

    project_files
     |- src
     |- tests
     |- lily_unit_test_reports              // generic report folder
         |- 20231220_14:37:17               // date and time of the test run
             |- 1_TestRunner.txt            // test runner log
             |- 2_Folder01Module01.txt      // test suite log
             |- 3_Folder01Module02.txt      // test suite log
             |- 4_Folder02Module03.txt      // test suite log
             |- 5_Folder02Module04.txt      // test suite log

These log files contain all messages from the test suite loggers.


## Test runner options

The test runner has the following options.

    from lily_unit_test import TestRunner

    options = {
        # Set the folder where the report is written to
        'report_folder': 'path/to/reports',

        # Creates a single HTML file with all the results
        # See example in: examples/example_report.html
        'create_html_report': True,
                
        # Open the HTML report in the default browser 
        'open_in_browser': True,
        
        # Do not write log files, in case using the HTML report 
        'no_log_files': True,

        # Run only the test suites in this list, skip others
        'include_test_suites': [
            'TestSuite01',
            'TestSuite02'
        ],

        # Do not run test suites in this list, do run others
        'exclude_test_suites': [
            'TestSuite03',
            'TestSuite04'
        ]
    }

    TestRunner.run('../src', options)


Because the options are in a dictionary, they can be easily read from a JSON file.
    
    import json
    from lily_unit_test import TestRunner

    TestRunner.run('../src', json.load(open('/path/to/json_file', 'r')))


This makes it easy to automate tests using different configurations.
