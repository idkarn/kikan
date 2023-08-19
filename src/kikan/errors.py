from sys import exc_info
from traceback import format_exception


class LaunchError(Exception):
    def __init__(self, *args):
        self.message = "Critical error was occured while launch."
        self.traceback = "".join(format_exception(*exc_info()))
        super().__init__(self.message)


class LoggerInitializationError(Exception):
    def __init__(self, *args):
        self.message = "Logger has not been initialized. Do it before printing."
        self.traceback = "".join(format_exception(*exc_info()))
        super().__init__(self.message)
