# Unit test package for Python

Unit test package for adding unit tests to your project.

### Release history:

This list shows the most recent releases:

* 202301: V1.3.0
  * test runner can have a classification for handling known issues.
* 202301: V1.2.0
  * test runner run method returns True when passed and False when failed.  
  * fixed package name in distribution
* 202312: V1.1.0
  * fix issue with writing HTML report if path does not exist 
* 202312: V1.0.0
  * official release


## Installation

Install from the Python package index:

`pip install lily-unit-test`

## Usage

Create a file: `my_class.py`

```python
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
```

Run the file: `python -m my_class.py`

The output should look like:

```
2023-12-20 19:28:46.105 | INFO   | Run test suite: MyTestSuite
2023-12-20 19:28:46.105 | INFO   | Run test case: MyTestSuite.test_add_one
2023-12-20 19:28:46.106 | INFO   | Test case MyTestSuite.test_add_one: PASSED
2023-12-20 19:28:46.106 | INFO   | Run test case: MyTestSuite.test_add_two
2023-12-20 19:28:46.106 | INFO   | Test case MyTestSuite.test_add_two: PASSED
2023-12-20 19:28:46.106 | INFO   | Test suite MyTestSuite: 2 of 2 test cases passed (100.0%)
2023-12-20 19:28:46.106 | INFO   | Test suite MyTestSuite: PASSED
```

## Test runner

A test runner is an object to run test suites from a specific folder recursively.

```python
from lily_unit_test import TestRunner

TestRunner.run('path/to/test_suites')
```

The test runner will create a folder with reports about the tests that were executed.
More details of the test runner are explained further in this document. 


# Test suite object

The test suite class is a base class that is used for all the test suites.
Test cases are created by adding test methods to the test suite.
These test methods are executed by the test suite run method.
Preceding the test cases, an optional setup method is executed.
If the setup fails, execution is stopped.
Following the test cases a teardown method will be executed,
regardless whether the test cases passed or failed.

## Test suite creation

Creating a test suite is a simple as creating a subclass:

```python
import lily_unit_test

class MyTestSuite(lily_unit_test.TestSuite):
    ...
```

Test cases are added using methods with the prefix: `test_`:

```python
import lily_unit_test

class MyTestSuite(lily_unit_test.TestSuite):
    
    def test_login(self):
        ...
    
    def test_upload_image(self):
        ...
```

In this case two test cases are defined.
The tests are executed in the order as they are created, from top to bottom.

## Using setup and teardown

The setup and teardown can be added to your test suite:

```python
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
```

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

```python
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
    # Pass or fail by return True or False
    return self.connection.is_connected()
```

## Logging messages

The test suite has a build in logger for logging messages.

```python
def test_login(self):
    # Info message
    self.log.info('Connect to server')
    self.connection = connect_to_server(user, password)
    
    # Debug message
    self.log.debug('Connection status: {}'.format(self.connection.is_connected())
    
    if not self.connection.is_connected()
        # Error message
        self.log.error('We are not connected')

    return self.connection.is_connected()
```

Note that logging an error message NOT automatically makes the test fail.

The log messages are only written to the console window and to an internal buffer.
The internal buffer can be accessed by using the logger's: `get_log_messages()` method.

```python
ts = MyTestSuite()
ts.run()

# get log messages
log_messages = ts.log.get_log_messages()
```

## Classification

The test suite object has a build in classification.
This can be set by the `CLASSIFICATION` attribute.

```python
import lily_unit_test

class MyTestSuite(lily_unit_test.TestSuite):
    
    CLASSIFICATION = <value>
```

The values are defined in a object called `Classification` and can be imported from the package.

```python
import lily_unit_test

# Regular test suite
class MyTestSuite01(lily_unit_test.TestSuite):
    
    # By default the value is PASS, so this is not necessary 
    CLASSIFICATION = lily_unit_test.Classification.PASS


# Test suite that we expect to fail
class MyTestSuite02(lily_unit_test.TestSuite):
    
    # Override the default value
    CLASSIFICATION = lily_unit_test.Classification.FAIL
```

The default value is `PASS`, and is usually suitable for most test suites.
This means in general there is no need to override this attribute.
Setting this attribute to `FAIL` will make the test suite pass in case of a failure.
All errors are logged as usual but the end result will be passed in case of a failure.
If the test suite passes, the test suite is marked as failed.

This situation is useful when the test fails because of a known issue,
and you want to accept the known issue. As long as the issue is there the test will pass.
When the issue is solved, the test fails, reminding you to restore the classification attribute.

The log messages will show this:

```
- No classification defined:
2024-01-05 19:35:54.328 | ERROR  | Test classification is not defined: None
2024-01-05 19:35:54.328 | ERROR  | Test suite TestSuiteClassification: FAILED

- Classification set to FAIL and test suite fails because of a known issue, but is accepted
2024-01-05 19:38:17.989 | INFO   | Test suite failed, but accepted because classification is set to FAIL
2024-01-05 19:38:17.989 | INFO   | Test suite TestSuiteClassification: PASSED

- Classification set to FAIL and test suite passes because of the known issue is solved
2024-01-05 19:39:46.530 | ERROR  | Test suite passed, but a failure was expected because classification is set to FAIL
2024-01-05 19:39:46.530 | ERROR  | Test suite TestSuiteClassification: FAILED
```


# Test runner object

The test runner collects and runs a number of test suites and
writes all the results to report files.

## Run the test runner

Running the test runner is a simple as:

```python
from lily_unit_test import TestRunner

TestRunner.run('path/to/test_suites')
```

## Collecting and running test suites

Test suites are recursively collected from the Python files in the given folder.
Given the following project structure:

```
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
```

The test_runner.py contains the following code:

```python
from lily_unit_test import TestRunner

TestRunner.run('../src')
```    

The test runner is located in the `./test` folder.
The test runner will run all tests in the folder: `../src`.
This is relative to the `test` folder. Be sure to run the test runner from the `test`folder.
You can also use an absolute path to the folder.

The test runner will scan all modules in the folder in `src` recursively.
This means all 4 python modules are checked for test suites.

The test runner imports each module and checks if the module contains a class that is
based on the test suite base class (`class MyTestSuite(lily_unit_test.TestSuite)`).

All test suites are executed in alphabetical order.
If a specific order is required, use numbers in the file and folder names to sort them.
The test runner will run all the test suites and will write report files to a folder.
The output folder will look like this:

```
project_files
 |- src
 |- tests
 |- lily_unit_test_reports              // generic report folder
     |- 20231220_143717                 // date and time of the test run
         |- 1_TestRunner.txt            // test runner log
         |- 2_Folder01Module01.txt      // test suite log
         |- 3_Folder01Module02.txt      // test suite log
         |- 4_Folder02Module03.txt      // test suite log
         |- 5_Folder02Module04.txt      // test suite log
```

These log files contain all messages from the test suite loggers.

## Test runner options

The test runner has the following options.

```python
from lily_unit_test import TestRunner

options = {
    # Set the folder where the report is written to
    'report_folder': 'path/to/reports',

    # Creates a single HTML file with all the results
    # See example in: examples/example_report.html
    'create_html_report': True,
            
    # Open the HTML report in the default browser 
    'open_in_browser': True,
    
    # Do not write log files, in case using the HTML report or other logging facilities
    'no_log_files': True,

    # Run only the test suites in this list, skip others
    # If the list is empty or omitted, all test suites are run
    'include_test_suites': [
        'TestSuite01',
        'TestSuite02'
    ],

    # Skip test suites in this list
    'exclude_test_suites': [
        'TestSuite03',
        'TestSuite04'
    ]
}

TestRunner.run('../src', options)
```

Because the options are in a dictionary, they can be easily read from a JSON file.

```python
import json
from lily_unit_test import TestRunner

TestRunner.run('../src', json.load(open('/path/to/json_file', 'r')))
```

This makes it easy to automate tests using different configurations.

(c) 2023 - LilyTronics (https://lilytronics.nl)

