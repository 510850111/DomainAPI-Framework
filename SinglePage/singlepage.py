# coding: utf-8
import inspect
from .args import Args
from flask import *
from flask.views import *
from .serializer import *
from .broadcast import Broadcast, Radio
app = Flask(__name__)
app.config['resources'] = {}
broadcast = Broadcast(app)
args_filter = Args(app)

def register(cls, endpoint=''):
    endpoint = endpoint
    view = cls.as_view(cls.__name__)
    cls.pk_list = {}
    resource_name = endpoint.replace('/', '')
    app.config['resources'].update({resource_name: cls})
    for method in cls.methods:
        lowcase_method = method.lower()
        try:
            func = getattr(cls, lowcase_method)
        except AttributeError as e:
            pass
        args = []
        defaults = []
        if inspect.getargspec(func)[0] is not None:
            args = [e for e in inspect.getargspec(func)[0] if e is not 'self']
        if inspect.getargspec(func)[3] is not None:
            defaults = [e for e in inspect.getargspec(
                func)[3] if e is not 'self']
        defaults_dict = dict([(arg, default)
                              for arg in args for default in defaults])
        for arg in args:
            cls.pk_list.update({lowcase_method: arg})
            app.add_url_rule(endpoint + '<' + arg + '>',
                             view_func=view,
                             defaults=defaults_dict,
                             methods=[method, ])
    cls.object = cls
    cls().add_args()
    app.add_url_rule(endpoint, view_func=view)

class SinglePage(View):
    """this is the base class of single page"""
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
    pk_list = {}
    data = None
    object = None
    extends_class = {}
    strcture = None
    # strcture = [
    #   {
    #       'put_in':'id','pwd'
    #       'put_put':'pwd'
    #       'post_in':'id',
    #       'post_out':'',
    #       'get':'pwd',
    #       'deled_in':''
    #       'deled_out':''
    #   }
    # ]

    def get(self, *args, **kargs):
        pass

    def post(self, *args, **kargs):
        pass

    def put(self, *args, **kargs):
        pass

    def delete(self, *args, **kargs):
        pass

    def create_object(self, parser=None, json=None):
        """
            将request数据注入到self实例
        """
        if parser:
            self.data = parser(self.data)
        if json:
            self.data = json
        class_dict = serializer.attr_dict_from_sqlalchemy(self)
        for item in class_dict:
            setattr(self, item, self.data[item])
        return self

    def make_links(self, response):
        """
        ~ 一个指向集合资源的 self 链接。
        ~ 如果集合是分页的，并且还有下一页，要有一个指向下一页的链接。 
        ~ 如果集合是分页的，并且还有上一页，要有一个指向上一页的链接。
        ~ 一个集合大小的指示符。
        """
        link = {}
        root = request.url_root[0:len(request.url_root) - 1]
        url = request.url
        base = request.base_url
        path = request.path
        next_url = ''
        prev_url = ''
        self_url = request.url
        args_str = url.replace(base, '')
        args_dict = request.args
        if args_dict.get('offset', None):
            next = args_dict.get('offset', None, type=int) + \
                args_dict.get('limit', None, type=int)
            perv = args_dict.get('offset', None, type=int) - \
                args_dict.get('limit', None, type=int)
            orgin_offset = 'offset=' + args_dict.get('offset', None)
            next_str = args_str.replace(orgin_offset, 'offset=' + str(next))
            prev_str = args_str.replace(orgin_offset, 'offset=' + str(perv))
            next_url = base + next_str
            prev_url = base + prev_str
        else:
            path_list = path.split('/')
            if path_list[-1] != '':
                try:
                    pk = int(path_list[-1])
                    loc = '/'.join(path_list[1:-1])
                    next = '/' + loc + '/' + str(pk + 1)
                    prev = '/' + loc + '/' + str(pk - 1)
                    next_url = root + next + args_str
                    prev_url = root + prev + args_str
                except:
                    pass
            else:
                next_url = self_url
                prev_url = self_url
        link.update({'count': response.count()})
        link.update({'self': self_url})
        link.update({'next': next_url})
        link.update({'prev': prev_url})
        return link

    def json_response(self, response, class_type):
        serializer = Serializer()
        if class_type == 'origin':
            return response
        if class_type == 'basic':
            response = {"data": response}
            # response.update(link_dict)
            return jsonify(response)
        if class_type == 'sqlalchemy':
            serializer.class_type = class_type
            serializer.register_structure(self, self.extends_class)
            # def generator():
                # yield '{"data":['
                # for r in response.yield_per(100):
                    # data = serializer.dump(r)
                    # yield json.dumps(data) + ','
                # yield '{}]}'
            if request.method == 'GET':
                link_dict = self.make_links(response)
                response = {'data': serializer.dump(response)}
                response.update(link_dict)
            else:
                response = {'data': serializer.dump(response)}
            return jsonify(response)
            # return Response(generator(), 200, {'Content-type':
            # 'application/json'})

    def dispatch_request(self, *args, **kwargs):
        global broadcast
        self.broadcast = broadcast
        if request.method == 'GET':
            if self.strcture:
                self.__exclude__ = self.strcture.get('get')
            if kwargs == {}:
                try:
                    kwargs = {self.pk_list['get']: None}
                except KeyError as e:
                    pass
            response, class_type = self.get(*args, **kwargs)
            return self.json_response(response, class_type)
        elif request.method == 'POST':
            if self.strcture:
                self.__exclude__ = self.strcture.get('post_in')
            if kwargs == {}:
                try:
                    kwargs = {self.pk_list['post']: None}
                except KeyError as e:
                    pass
            response, class_type = self.post(*args, **kwargs)
            if self.strcture:
                self.__exclude__ = self.strcture.get('post_out')
            return self.json_response(response, class_type)
        elif request.method == 'PUT':
            if self.strcture:
                self.__exclude__ = self.strcture.get('put_in')
            if kwargs == {}:
                try:
                    kwargs = {self.pk_list['put']: None}
                except KeyError as e:
                    pass
            response, class_type = self.put(*args, **kwargs)
            if self.strcture:
                self.__exclude__ = self.strcture.get('put_out')
            return self.json_response(response, class_type)
        elif request.method == 'DELETE':
            if self.strcture:
                self.__exclude__ = self.strcture.get('delete_in')
            if kwargs == {}:
                try:
                    kwargs = {self.pk_list['delete']: None}
                except KeyError as e:
                    pass
            response, class_type = self.delete(*args, **kwargs)
            if self.strcture:
                self.__exclude__ = self.strcture.get('delete_out')
            return self.json_response(response, class_type)
