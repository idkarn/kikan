from sys import exc_info
from traceback import format_exception


class LaunchError(Exception):
    def __init__(self, *args: object) -> None:
        self.message = f"Critical error was occured while launch"
        self.traceback = "".join(format_exception(*exc_info()))
        super().__init__(self.message)
