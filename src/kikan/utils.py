from inspect import isfunction

from kikan.events import InitEvent


class ArgumentsHelper:
    #! suitability in question
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

    def __init__(self, output_file: str):
        self.ouput_file = open(output_file, "w")
        self.buffer: list[str] = []  # TODO: make this a queue

        # one thread (main thread that calls print())
        # adds the the buffer (pushes to the queue)

        # another thread (optional!) (calls _flush() every
        # now and then (with thread.sleep or something))

        # https://docs.python.org/3/library/threading.html#event-objects

        # if self.multithreading:
        #     self._flush_thread = \
        #         threading.thread(self._run_flush_thread)

    def _run_flush_event(self):
        while self._stop_event.wait(timeout=1):
            # ^ blocks until the event is set
            #   maximum for 'timeout' seconds
            #   returns True if the flag is set
            # so the flushes happen every second
            self._flush()

    def close(self):
        # set a flag to show that the file is closed
        # see https://www.pythontutorial.net/python-concurrency/python-threading-event/
        # self._stop_event.set()
        # self._flush_thread.join()
        self.output_file.close()

    def _flush(self):
        buf = self.buffer.copy()
        for msg in buf:
            self.ouput_file.write(msg)

    def print(self, *args, end='\n', sep=' '):
        self.buffer.append(sep.join(args) + end)
        # if not self.multithreading:
        self._flush()

    @InitEvent.trigger
    @staticmethod
    def init():
        if hasattr(Logger, "deinit"):
            print("Logger.default already exists")
            return
        Logger.default = Logger("default.log")

    # @DeInitEvent.trigger
    @staticmethod
    def deinit():
        if hasattr(Logger, "default"):
            Logger.default.close()
