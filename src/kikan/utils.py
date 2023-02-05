from inspect import isfunction


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
