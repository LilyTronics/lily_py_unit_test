# Test suite

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
    
