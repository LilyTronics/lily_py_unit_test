# Unit test package for Python

Unit test package for adding unit tests to your project.

### Roadmap:

* 202312/202401: Publish to PyPi

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

## Test suite object

Using the test suite as an object:
    
    # Test suite from previous example
    ts = MyTestSuite()
    
    # Run method returns True if passed else False
    result = ts.run()
    print('Test passed:', result)

    # Write log messages to file:
    with open('test_report.txt', 'w') as fp:
        # Write every message on a new line, the Pythonic way:
        fp.writelines(map(lambda x: '{}\n'.format(x), ts.log.get_log_messages()))

        # You could also use a loop (less Pythonic):
        # for message in ts.log.get_log_messages():
        #     fp.write('{}\n'.format(message))

See test_suite.md for more details


## Test runner

A test runner is an object to run test suites from a specific folder recursive.

    from lily_unit_test import TestRunner

    TestRunner.run('path/to/test_suites')

See test_runner.md for more details


(c) 2023 - LilyTronics (https://lilytronics.nl)

