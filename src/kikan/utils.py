class LaunchError(RuntimeError):
    ...


class InitData:  # temp objects that store all data of real objects for engine init phase
    def __init__(self, cls, *args):
        self.cls = cls
        self.args = args
