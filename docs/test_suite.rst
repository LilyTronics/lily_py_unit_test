The test suite
==============

This page describes more details about the test suite class.

The test suite class is the main class for running tests.
Each test case is defined as a method in the test suite.
The method must start with :code:`test_`.
These test methods are executed when the test suite is executed.

Preceding the test methods, a setup method is executed.
If the setup fails, execution is stopped.
Following the test methods a teardown method is executed.
The teardown method is always executed, regardless whether the test methods passed or failed.

Test suite creation
-------------------

Creating a test suite is as simple as creating a subclass:

.. code-block:: python

    import lily_unit_test

    class MyTestSuite(lily_unit_test.TestSuite):
        # My test suite

Test methods are added by adding methods with the prefix: :code:`test_`:

.. code-block:: python

    import lily_unit_test

    class MyTestSuite(lily_unit_test.TestSuite):

        def test_login(self):
            # test log in

        def test_upload_image(self):
            # test uploading image

In this case two test methods are defined.
The test methods are executed in the order as they are created, from top to bottom.

Other methods can also be added to the test suite to provide specific functionality.

.. code-block:: python

    import lily_unit_test

    class MyTestSuite(lily_unit_test.TestSuite):

        def connect_to_server()
            # connect to server

        def test_login(self):
            self.connect_to_server()
            # test log in

        def test_upload_image(self):
            self.connect_to_server()
            # test uploading image

In this test suite we added a helper method to connect to the server. We use this in each test method to connect
to a server before doing the tests. The connect to server method, does not start with :code:`test_` and is ignored
by the test suite when it is executed.

Running the test suite
----------------------

The test suite can be executed using the :code:`run` method.
The :code:`run` method returns :code:`True` if the test suite passed and :code:`False` if failed.
In order to make the test suite run properly, the test suite must be initialized:

.. code-block:: python

    # Initialize test suite, the test suite require any parameters
    ts = MyTestSuite()
    # Run the test suite
    ts.run()

    # A nice one liner
    MyTestSuite().run()

    # Using the test result
    if MyTestSuite().run():
        print("Yay, the test suite passed!")
    else:
        print("Oops, the test suite failed...")

Using setup and teardown
------------------------

The test suite has a default setup and teardown methods that can be overridden in the subclass.
The default setup and teardown do nothing, they are just empty methods.
If not overridden, it will not matter.
The setup and teardown can be overridden in your test suite:

.. code-block:: python

    import lily_unit_test

    class MyTestSuite(lily_unit_test.TestSuite):

        connection = None

        def setup(self):
            self.connection = connect_to_server(user, password)

        def test_upload_image(self):
            self.connection.upload_image(filename)

        def test_download_image(self):
            self.connection.download_image(uri, filename)

        def teardown(self):
            # In case the connection could not be created, the connection property could still be None
            if self.connection is not None and self.connection.is_connected():
                self.connection.close()

In this hypothetical example, prior to all tests a connection to a server is created in the setup method.
In case this fails because of an exception, the execution stops and the test suite fails.
In case the setup method passes, the test methods will be executed.
Finally, the teardown is executed. The teardown closes the connection with the server.
If in the hypothetical case, the connection was not established in the setup (failed for some reason),
closing a not established connection can cause an exception.
The test suite will fail if the teardown fails because of an exception.

Making test suites pass or fail
-------------------------------

A test method or setup method is passed by the following conditions:

* There were no exceptions or asserts.
* There were no messages from the standard error handler (stderr).
* The return value is None (default return value of a method) or True.

A test method or setup method is failed by the following conditions:

* An exception or assert was raised
* There were messages from the standard error handler (stderr).
* The return value is False

The teardown method can only fail if an exception or assert was raised. The return value is not used.

The return value of a method in Python is by default :code:`None`. If the test method is executed and the return value
is :code:`None`, the test method is marked as passed. If yu wish to explicitly make a method fail, you can return
:code:`False`. The test suite will mark the test method as failed.

The test suite checks for messages from the standard error handler (stderr).
There can be threads running in the background that generate exceptions. These exceptions cannot be caught by the
test suite. But these exceptions will generate messages to the standard error handler. These messages are used for
the test suite result.

Examples of passing or failing test suites
------------------------------------------

The following examples only show the specific test method from the test suite.

.. code-block:: python

    # Fails in case an exception in the connect to server method is raised
    def test_login(self):
        self.connection = connect_to_server(user, password)

    # Fail by using an assert
    def test_login(self):
        self.connection = connect_to_server(user, password)
        assert self.connection.is_connected(), "We are not connected"

    # Fail by raising an exception if we are not connected
    def test_login(self):
        self.connection = connect_to_server(user, password)
        if not self.connection.is_connected():
            raise Exception("We are not connected")

    # Fail by using the build-in fail method
    def test_login(self):
        self.connection = connect_to_server(user, password)
        if not self.connection.is_connected():
            self.fail("We are not connected")

    # Preferred way: fail by using the build-in fail_if method
    def test_login(self):
        self.connection = connect_to_server(user, password)
        self.fail_if(not self.connection.is_connected(), "We are not connected")

    # Pass or fail by return True or False
    def test_login(self):
        self.connection = connect_to_server(user, password)
        return self.connection.is_connected()

The preferred way of letting a test suit pass or fail is using the fail_if method.
Usually passing or failing will depend on the result of some action (executing a function, comparing a variable).
The fail_if method also has a way of controlling if the test suite should continue or should be aborted.
More details in the API section of this document.

Logging messages
----------------

The test suite has a build in logger for logging messages.
Log messages are stored in an internal buffer (a list with strings)
and are directly written to the standard output (stdout, usually the console).
Messages from the standard output and error handler (stdout and stderr),
are redirected to the logger. When using :code:`print()`, the output is stored in the logger.
If an exception is raised, the trace message from the exception is stored in the logger.
The logger can be accessed by the log attribute of the test suite:

.. code-block:: python

    import lily_unit_test

    class MyTestSuite(lily_unit_test.TestSuite):

        def test_something(self):
            # Write a log message
            self.log.info("Start test something")

Before and after running th test suite, the logger is also available:

.. code-block:: python

    # Initialize the test suite
    ts = MyTestSuite()

    ts.log.info("This is a message before running the test suite")

    ts.run()

    ts.log.info("This is a message after running the test suite")

Below some examples of log messages.

.. code-block:: python

    def test_login(self):
        # Info message
        self.log.info("Connect to server")
        self.connection = connect_to_server(user, password)

        # Debug message
        self.log.debug("Connection status: {}".format(self.connection.is_connected())

        # Let's check the connection properties using print
        # These messages will be written automatically to the logger
        # This can be useful for a quick logging of some variables
        print("Server IP  :", self.connection.get_server_ip())
        print("Server name:", self.connection.get_server_name())

        # Insert an empty line
        self.log.empty_line()

        if not self.connection.is_connected()
            # Error message
            self.log.error("We are not connected")

        return self.connection.is_connected()

Note that logging an error message NOT automatically makes the test fail.

It is possible to get the messages from the logger:

.. code-block:: python

    ts = MyTestSuite()
    ts.run()

    # Get the log messages
    messages = ts.log.get_log_messages()
    # Write to file
    with open("test_report.txt", "w") as fp:
        # The messages is a list, we can write the list in one time
        fp.writelines(messages)

See the logger API documentation for more details.

Classification
--------------

The test suite object has a build in classification.
This can be set by the :code:`CLASSIFICATION` attribute.

.. code-block:: python

    import lily_unit_test

    class MyTestSuite(lily_unit_test.TestSuite):

        CLASSIFICATION = <value>

The values are defined in an object called :code:`Classification` and can be imported from the package.

.. code-block:: python

    import lily_unit_test

    # Regular test suite
    class MyTestSuite01(lily_unit_test.TestSuite):

        # By default the value is PASS, so this is not necessary
        CLASSIFICATION = lily_unit_test.Classification.PASS


    # Test suite that we expect to fail
    class MyTestSuite02(lily_unit_test.TestSuite):

        # Override the default value
        CLASSIFICATION = lily_unit_test.Classification.FAIL

The default value is :code:`PASS`, and is usually suitable for most test suites.
This means in general there is no need to override this attribute.
Setting this attribute to :code:`FAIL` will make the test suite pass in case of a failure.
All errors are logged as usual but the end result will be passed in case of a failure.
If the test suite passes, the test suite is marked as failed.

This situation is useful when the test fails because of a known issue,
and you want to accept the known issue. As long as the issue is there the test will pass.
When the issue is solved, the test fails, reminding you to restore the classification attribute.

The log messages will show this:

.. code-block:: console

    - No classification defined:
    2024-01-05 19:35:54.328 | ERROR  | Test classification is not defined: None
    2024-01-05 19:35:54.328 | ERROR  | Test suite TestSuiteClassification: FAILED

    - Classification set to FAIL and test suite fails because of a known issue, but is accepted
    2024-01-05 19:38:17.989 | INFO   | Test suite failed, but accepted because classification is set to 'FAIL'
    2024-01-05 19:38:17.989 | INFO   | Test suite TestSuiteClassification: PASSED

    - Classification set to FAIL and test suite passes because of the known issue is solved
    2024-01-05 19:39:46.530 | ERROR  | Test suite passed, but a failure was expected because classification is set to 'FAIL'
    2024-01-05 19:39:46.530 | ERROR  | Test suite TestSuiteClassification: FAILED

Subclassing the test suite
--------------------------

You can create your own sub class of the test suite and use that test suite sub class for running tests.
This provides a way for adding your own test functions you can use in all your test suites.
An example of creating your own test suite base class is shown below:

.. code-block:: python

    import lily_unit_test

    # First we create our own test suite base class, which is a subclass of the lily test suite
    class MyTestSuiteBaseClass(lily_unit_test.TestSuite):

        # Override constructor, not needed in some cases
        # Can be needed when we need to initialize stuff before running the test suite
        def __init__(self, *args):
            # initialize the lily Test Suite with parameters
            super().__init__(*args)

            # Add our own stuff to initialize
            self.my_attribute = some_value

        # Add some methods to use in your test suites
        def calculate_something_important(self):
            # Here some amazing code where we calculate something very important.


    # Use our own test suite
    class MyTestSuite(MyTestSuiteBaseClass):

        def test_something(self):
            # Access the added attribute
            self.my_attribute = a_new_value
            # Do some calculations
            self.calculate_something_important()


    # Run the test suite
    if __name__ == "__main__":

        MyTestSuite().run()

This can help you prevent duplicate code in your tests and make your test suites more maintainable.

There is a small catch. When using the test runner, it will search for any class based on the lily test suite class.
Meaning in our example, it will run two test suites: MyTestSuiteBaseClass and MyTestSuite.
We cannot know that MyTestSuiteBaseClass is not a test suite but only used as base class.
To prevent running the base class, simply add it as an exclusion to the test runner:

.. code-block:: python

    from lily_unit_test import TestRunner

    # Run test runner with the base class excluded
    options = {
        "exclude_test_suites": ["MyTestSuiteBaseClass"]
    }
    TestRunner.run(".", options)

For more details about using the test runner, see the chapter about the test runner.

Test suite API
------------------

.. currentmodule:: lily_unit_test

.. autoclass:: TestSuite
    :members: run, get_report_path, setup, teardown, fail, fail_if, sleep, start_thread, wait_for
