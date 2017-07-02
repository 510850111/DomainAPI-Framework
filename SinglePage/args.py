from .utils import singleton


@singleton
class Args():
    __args = {}
    app = None

    def __init__(self, app):
        self.app = app

    def add_args(self, arg_dict):
        self.__args.update(arg_dict)

    def remove_args(self, arg_key):
        self.__args.remove(arg_key)

    def get_args(self):
        return self.__args

    def run_arg(self, arg_key, request_args):
        if arg_key in self.__args:
           func = self.get_args(arg_key)
        try:
            func()
        except Exception as e:
            if app and app.debug:
                print('args got a err \'{}\''.format(arg_key))                
            raise e
        