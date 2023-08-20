import os
import time
from datetime import datetime
from inspect import isfunction

from kikan.errors import LoggerInitializationError


class ArgumentsHelper:
    # ! suitability in question
    """ __init__ method decorator for helping to use other decorators with calling `@Example(foo="bar")` or without directly calling `@Example"""

    def __init__(self, fn: callable) -> None:
        self.__wrapped_init = fn

    def __set_name__(self, owner, name):
        owner_init = self.__wrapped_init

        def wrapper(self, *args, **kwargs):
            if len(args) > 1:
                raise ValueError("Too many arguments")
            elif len(args) == 1 and isfunction(args[0]):
                self._wrapped_method = args[0]

                def set_name(self, owner, name):
                    setattr(owner, name, self._wrapped_method)

                setattr(owner, "__set_name__", set_name)

                owner_init(self, *args, **kwargs)
            else:
                def call_class(self, fn):
                    self._wrapped_method = fn
                    owner_init(self, *args, **kwargs)
                    return fn

                setattr(owner, "__call__", call_class)

        setattr(owner, name, wrapper)


class InitData:  # temp objects that store all data of real objects for engine init phase
    def __init__(self, cls, *args):
        self.cls = cls
        self.args = args


class Logger:
    default: "Logger"
    HEADING_LENGTH = 70

    def __init__(self):
        if 'logs' not in os.listdir():
            os.mkdir('logs')
        logs = [int(f[6:-4]) for f in os.listdir('logs')
                if f.startswith('group_') and f.endswith('.log') and f[6:-4].isdigit()]
        if not logs:
            self.main_file = open(f'logs/group_1.log', 'w')
            self.last_group_number = 1
            self.lines_in_log = 0
        else:
            self.last_group_number = max(logs)
            self.main_file = open(
                f'logs/group_{self.last_group_number}.log', 'r+')
            self.lines_in_log = len(self.main_file.readlines())
        self.check_log_overflow()

        self.latest_log_file = open('logs/latest.log', "w")

        self.buffer: list[str] = []  # TODO: make this a queue
        self.first_print = True

        # one thread (main thread that calls print())
        # adds the the buffer (pushes to the queue)

        # another thread (optional!) (calls _flush() every
        # now and then (with thread.sleep or something))

        # https://docs.python.org/3/library/threading.html#event-objects

        # if self.multithreading:
        #     self._flush_thread = \
        #         threading.thread(self._run_flush_thread)

    def check_log_overflow(self):
        if self.lines_in_log >= 5000:
            self.main_file.close()
            self.lines_in_log = 0
            self.last_group_number += 1
            self.main_file = open(
                f'logs/group_{self.last_group_number}.log', 'w')

    # def _run_flush_event(self):
    #     while self._stop_event.wait(timeout=1):
    #         # ^ blocks until the event is set
    #         #   maximum for 'timeout' seconds
    #         #   returns True if the flag is set
    #         # so the flushes happen every second
    #         self._flush()

    def close(self):
        # set a flag to show that the file is closed
        # see https://www.pythontutorial.net/python-concurrency/python-threading-event/
        # self._stop_event.set()
        # self._flush_thread.join()
        self.main_file.close()
        self.latest_log_file.close()

    def _flush(self):
        buf = self.buffer.copy()
        self.buffer.clear()
        for msg in buf:
            self.main_file.write(msg)
            self.latest_log_file.write(msg)
        self.main_file.flush()
        self.latest_log_file.flush()

    def print_(self, *args, end='\n', sep=' ', hide_time_stamp=False):
        if self.first_print:
            self.first_print = False
            self.start_session()
        msg = sep.join([str(item) for item in args]) + end
        self.buffer.append(
            msg if hide_time_stamp else f"[{datetime.now().astimezone().isoformat()}] {msg}")
        # if not self.multithreading:
        self._flush()

        self.lines_in_log += msg.count('\n')
        self.check_log_overflow()

    @staticmethod
    def print(*args, end='\n', sep=' ', hide_time_stamp=False):
        try:
            Logger.default.print_(*args, end=end, sep=sep,
                                  hide_time_stamp=hide_time_stamp)
        except AttributeError:
            raise LoggerInitializationError

    def start_session(self):
        self.print_('=' * Logger.HEADING_LENGTH, hide_time_stamp=True)
        time_msg = ' ' + time.ctime() + ' '
        self.print_(time_msg.center(Logger.HEADING_LENGTH, '='),
                    hide_time_stamp=True)
        self.print_('=' * Logger.HEADING_LENGTH, hide_time_stamp=True)

    @staticmethod
    def init():
        if hasattr(Logger, "default"):
            Logger.print("Logger.default already exists")
            return
        Logger.default = Logger()

    # @DeInitEvent.trigger
    @staticmethod
    def terminate():
        if hasattr(Logger, "default"):
            Logger.default.close()
            delattr(Logger, "default")
