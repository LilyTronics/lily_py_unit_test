# Unit test package for Python

Unit test package for adding unit tests to your project.

### Release history:

* 202312: V1.1.0 fix issue with writing HTML report if path does not exist 
* 202312: V1.0.0 official release


## Installation

Install from the Python package index:

`pip install lily_unit_test`

## Usage

Create a file: `my_class.py`

    """
    This example shows how to run a simple unit test.
    """
    
    import lily_unit_test
    
    
    class MyClass(object):
        """
        Your class that will do something amazing.
        """
    
        @staticmethod
        def add_one(x):
            return x + 1
    
        @staticmethod
        def add_two(x):
            return x + 2
    
    
    class MyTestSuite(lily_unit_test.TestSuite):
        """
        The test suite for testing MyClass.
        """
    
        @staticmethod
        def test_add_one():
            assert MyClass.add_one(3) == 4, 'Wrong return value'
    
        @staticmethod
        def test_add_two():
            assert MyClass.add_two(3) == 5, 'Wrong return value'
    
    
    if __name__ == '__main__':
        """
        Run the test code, when not imported.
        """
    
        MyTestSuite().run()

Run the file: `python -m my_class.py`

The output should look like:

    2023-12-20 09:28:46.105 | INFO   | Run test suite: MyTestSuite
    2023-12-20 09:28:46.105 | INFO   | Run test case: MyTestSuite.test_add_one
    2023-12-20 09:28:46.106 | INFO   | Test case MyTestSuite.test_add_one: PASSED
    2023-12-20 09:28:46.106 | INFO   | Run test case: MyTestSuite.test_add_two
    2023-12-20 09:28:46.106 | INFO   | Test case MyTestSuite.test_add_two: PASSED
    2023-12-20 09:28:46.106 | INFO   | Test suite MyTestSuite: 2 of 2 test cases passed (100.0%)
    2023-12-20 09:28:46.106 | INFO   | Test suite MyTestSuite: PASSED


## Test runner

A test runner is an object to run test suites from a specific folder recursive.

    from lily_unit_test import TestRunner

    TestRunner.run('path/to/test_suites')


# Test suite object

The test suite class is a base class that is used for all the test suites.
Test cases are created by adding test methods to the test suite.
These test methods are executed by the test suite run method.
Preceding the test cases, an optional setup method is executed.
If the setup fails, execution is stopped.
Following the test cases a teardown method will be executed,
regardless whether the test cases are passed or failed.


## Test suite creation

Creating a test suite is a simple as creating a subclass:

    import lily_unit_test

    class MyTestSuite(lily_unit_test.TestSuite):
        ...

Test cases are added using methods with the prefix: `test_`:

    import lily_unit_test

    class MyTestSuite(lily_unit_test.TestSuite):
        
        def test_login(self):
            ...
        
        def test_upload_image(self):
            ...

In this case two test cases are defined.
Note that test case methods are executed in alphabetical order.
In case order is important, you can use numbers in your test case methods:

    import lily_unit_test

    class MyTestSuite(lily_unit_test.TestSuite):
        
        def test_01_login(self):
            ...
        
        def test_02_upload_image(self):
            ...


## Using setup and teardown

The setup and teardown can be added to your test suite:

    import lily_unit_test

    class MyTestSuite(lily_unit_test.TestSuite):
        
        def setup(self):
            self.connection = connect_to_server(user, password)
        
        def test_upload_image(self):
            self.connection.upload_image(filename)
        
        def test_download_image(self):
            self.connection.download_image(uri, filename)

        def teardown(self):
            self.connection.close()

In this hypothetical example, prior to all tests a connection to a server is created.
In case this fails because of an exception, the execution stops and the test suite fails.
In case the setup passes, the test cases will be executed.
Finally, the teardown is executed. The teardown closes the connection with the server.


## Making test suites pass or fail

A test case method or setup method is passed by the following conditions:

* There were no exceptions or asserts.
* The return value is None or True.

A test case method or setup method is failed by the following conditions:

* An exception or assert was raised
* The return value is False

The teardown can only fail if an exception or assert was raise.
The return value is not used.


## Examples of passing or failing test suites

The following examples only show the specific test method from the test suite.

    def test_login(self):
        # Setup that fails by exception from the connect to server method
        self.connection = connect_to_server(user, password)
        # The return value is by default None

    def test_login(self):
        self.connection = connect_to_server(user, password)
        # Fail by raising an exception
        if not self.connection.is_connected():
            raise Exception('We are not connected')
        # The return value is by default None

    def test_login(self):
        self.connection = connect_to_server(user, password)
        # Fail by assert
        assert self.connection.is_connected(), 'We are not connected'
        # The return value is by default None

    def test_login(self):
        self.connection = connect_to_server(user, password)
        # Fail by return True or False
        return self.connection.is_connected()


## Logging messages

The test suite has a build in logger for logging messages.

    def test_login(self):
        # Info message
        self.log.info('Connect to server')
        self.connection = connect_to_server(user, password)
        
        # Debug message
        self.log.debug('Connection status: {}'.format(self.connection.is_connected())
        
        if not self.connection.is_connected()
            # Error message
            self.log.error('We are not connected')


Note that logging an error message NOT automatically makes the test fail.

The log messages are only written to the console window and to an internal buffer.
The internal buffer can be accessed by using the logger's: `get_log_messages()` method.

    ts = MyTestSuite()
    ts.run()
    
    # get log messages
    log_messages = ts.log.get_log_messages()
    

# Test runner object

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

(c) 2023 - LilyTronics (https://lilytronics.nl)

