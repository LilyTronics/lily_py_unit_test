"""
Logger for the application.
"""

import sys
import threading
import time

from datetime import datetime


class Logger(object):

    TYPE_INFO = 'INFO'
    TYPE_DEBUG = 'DEBUG'
    TYPE_ERROR = 'ERROR'
    TYPE_STDOUT = 'STDOUT'
    TYPE_STDERR = 'STDERR'
    TYPE_EMPTY_LINE = 'EMPTY_LINE'

    TIME_STAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    _LOG_FORMAT = '{} | {:6} | {}'

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
        self._output = ''

        self._orgStdout = sys.stdout
        self._orgStderr = sys.stderr
        if redirect_std:
            sys.stdout = self._StdLogger(self, self.TYPE_STDOUT)
            sys.stderr = self._StdLogger(self, self.TYPE_STDERR)

    def get_log_messages(self):
        return self._log_messages

    def shutdown(self):
        sys.stdout = self._orgStdout
        sys.stderr = self._orgStderr

    def info(self, message):
        self.handle_message(self.TYPE_INFO, '{}\n'.format(message))

    def debug(self, message):
        self.handle_message(self.TYPE_DEBUG, '{}\n'.format(message))

    def error(self, message):
        self.handle_message(self.TYPE_ERROR, '{}\n'.format(message))

    def empty_line(self):
        self.handle_message(self.TYPE_EMPTY_LINE, '')

    def handle_message(self, message_type, message_text):
        if message_type == self.TYPE_EMPTY_LINE:
            self._log_messages.append('')
            if self._log_to_stdout:
                self._orgStdout.write('\n')

        else:
            timestamp = datetime.now().strftime(self.TIME_STAMP_FORMAT)[:-3]
            self._output += message_text
            while '\n' in self._output:
                index = self._output.find('\n')
                line = self._LOG_FORMAT.format(timestamp, message_type, self._output[:index])
                self._output = self._output[index + 1:]
                self._log_messages.append(line)
                if self._log_to_stdout:
                    self._orgStdout.write('{}\n'.format(line))


if __name__ == "__main__":

    def _generate_error():
        def _exception(): _dummy = 1 / 0

        t = threading.Thread(target=_exception)
        t.start()
        time.sleep(1)


    test_logger = Logger()
    test_logger.info('This is an info message.')
    test_logger.debug('This is a debug message.')
    test_logger.error('This is an error message.')

    print('This is a stdout message.')
    print('This is a\nmulti line message.')

    _generate_error()

    test_logger.shutdown()

    print('\nMessages from logger')
    for log_message in test_logger.get_log_messages():
        print(log_message)
