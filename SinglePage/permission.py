class permission(object):

    def get(self, pk=None, handler=None):
        'get permission'
        return True, None, 200

    def post(self, handler=None):
        'post permission'
        return True, None, 200

    def put(self, handler=None):
        'put permission'
        return True, None, 200

    def delete(self, handler=None):
        'delete permission'
        return True, None, 200
