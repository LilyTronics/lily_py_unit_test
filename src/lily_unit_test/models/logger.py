"""
Logger for the application.
"""

import sys
import threading
import time

from datetime import datetime


class Logger(object):
    """
    Logger class.
    Handles all log messages and messages from stdout and stderr.
    The logger is part of the test suite and can be accessed by: :code:`TestSuite.log`.

    :param redirect_std: if True, stdout and stderr are redirected to the logger.
    :param log_to_stdout: if True, log messages are written to the stdout (console).

    | All log messages are stored to an internal buffer (list of strings).
    | All log messages have the following format:

    :code:`"<timestamp> | <type> | <message>"`

    | :code:`<timestamp>`: date and time of the message. Time is up to 1ms accurate.
    | :code:`<type>`: Type of the message.
    | :code:`<message>`: The message itself.

    The message type can have one of the following values:

    ======== =================================================================================
    Type     Description
    ======== =================================================================================
    | INFO   | Informational message, usually for indicating generic test messages.
    | DEBUG  | Debug message, usually for logging content of variables or more detailed test
             | messages.
    | ERROR  | Error message, for reporting an error.
    | STDOUT | Standard output messages, messages that are written to standard output handler,
             | usually when using :code:`print()`.
    | STDERR | Standard error messages, messages that are written to standard error handler,
             | usually when an exception is raised.
    ======== =================================================================================
    """

    TYPE_INFO = "INFO"
    TYPE_DEBUG = "DEBUG"
    TYPE_ERROR = "ERROR"
    TYPE_STDOUT = "STDOUT"
    TYPE_STDERR = "STDERR"
    TYPE_EMPTY_LINE = "EMPTY_LINE"

    TIME_STAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    _LOG_FORMAT = "{} | {:6} | {}"

    class _StdLogger(object):

        def __init__(self, logger, std_type):
            self._logger = logger
            self._type = std_type

        def write(self, message):
            self._logger.handle_message(self._type, message)

        def flush(self):
            pass

    def __init__(self, redirect_std=True, log_to_stdout=True):
        self._log_to_stdout = log_to_stdout
        self._log_messages = []
        self._output = ""

        self._orgStdout = sys.stdout
        self._orgStderr = sys.stderr
        if redirect_std:
            sys.stdout = self._StdLogger(self, self.TYPE_STDOUT)
            sys.stderr = self._StdLogger(self, self.TYPE_STDERR)

    def get_log_messages(self):
        """
        Returns a reference to the log messages buffer.

        :return: reference to the list of strings containing all log messages.

        | Note that it returns a reference, meaning any changes the logger makes to the list will affect the reference.
        | To get a static copy of the log messages use: :code:`get_log_messages().copy()`.
        | This will return a new list with a copy of all the log messages at that moment.
        """
        return self._log_messages

    def shutdown(self):
        """
        Shutdown the logger.
        This will restore the original stdout and stderr handlers.
        """
        sys.stdout = self._orgStdout
        sys.stderr = self._orgStderr

    def info(self, message):
        """
        Log a 'info' type message.

        :param message: the message to write to the logger.
        """
        self.handle_message(self.TYPE_INFO, "{}\n".format(message))

    def debug(self, message):
        """
        Log a 'debug' type message.

        :param message: the message to write to the logger.
        """
        self.handle_message(self.TYPE_DEBUG, "{}\n".format(message))

    def error(self, message):
        """
        Log a 'error' type message.

        :param message: the message to write to the logger.
        """
        self.handle_message(self.TYPE_ERROR, "{}\n".format(message))

    def empty_line(self):
        """
        Adds an empty line in the log messages.
        """
        self.handle_message(self.TYPE_EMPTY_LINE, "")

    def handle_message(self, message_type, message_text):
        """
        Handles the message of a given type. This method is use by :code:`info()`, :code:`debug()`, :code:`error()` and
        :code:`empty_line()`. It is not encouraged to use this function, use with caution.

        :param message_type: a string indicating the message type (see table above).
        :param message_text: the message to write to the logger.
        """
        if message_type == self.TYPE_EMPTY_LINE:
            self._log_messages.append("")
            if self._log_to_stdout:
                self._orgStdout.write("\n")

        else:
            timestamp = datetime.now().strftime(self.TIME_STAMP_FORMAT)[:-3]
            self._output += message_text
            while "\n" in self._output:
                index = self._output.find("\n")
                line = self._LOG_FORMAT.format(timestamp, message_type, self._output[:index])
                self._output = self._output[index + 1:]
                self._log_messages.append(line)
                if self._log_to_stdout:
                    self._orgStdout.write("{}\n".format(line))


if __name__ == "__main__":

    def _generate_error():
        def _exception(): _dummy = 1 / 0

        t = threading.Thread(target=_exception)
        t.start()
        time.sleep(1)


    test_logger = Logger()
    test_logger.info("This is an info message.")
    test_logger.debug("This is a debug message.")
    test_logger.error("This is an error message.")

    print("This is a stdout message.")
    print("This is a\nmulti line message.")

    _generate_error()

    test_logger.shutdown()

    print("\nMessages from logger")
    for log_message in test_logger.get_log_messages():
        print(log_message)
