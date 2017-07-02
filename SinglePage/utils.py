def singleton(cls, *args, **kw):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


class log:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def warning(info, need_string):
        string = log.WARNING + info + log.ENDC
        if not need_string:
            print(string)
        else:
            return string

    @staticmethod
    def header(info, need_string):
        string = log.HEADER + info + log.ENDC
        if not need_string:
            print(string)
        else:
            return string

    @staticmethod
    def blue(info, need_string):
        string = log.OKBLUE + info + log.ENDC
        if not need_string:
            print(string)
        else:
            return string

    @staticmethod
    def green(info, need_string):
        string = log.OKGREEN + info + log.ENDC
        if not need_string:
            print(string)
        else:
            return string

    @staticmethod
    def fail(info, need_string):
        string = log.FAIL + info + log.ENDC
        if not need_string:
            print(string)
        else:
            return string
