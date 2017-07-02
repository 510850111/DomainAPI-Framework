# coding:utf-8
from .permission import permission
from .serializer import serializer
from sqlalchemy import text, desc
from sqlalchemy.orm import joinedload, load_only, subqueryload, lazyload
from .singlepage import SinglePage
from .singlepage import *


class GeneralViewWithSQLAlchemy(SinglePage):
    """singlepage with SQLalchemy ORM"""

    db_session = None
    real_delete = True
    permissions = [permission]
    
    class args_filter():
        
        args = []

    def add_args(self):
        """
        this is use for add args and the child will reload this, 
        and this fuc will add some default args 
        """
        pass

    def set_permission(self, permission):
        self.permissions = permission

    def permission_layer(self, *args, **kwargs):
        # try:
        if self.permissions:
            for permission in self.permissions:
                if request.method == 'PUT':
                    permission().put(self, *args, **kwargs)
                if request.method == 'GET':
                    permission().get(self, *args, **kwargs)
                if request.method == 'POST':
                    permission().post(self, *args, **kwargs)
                if request.method == 'DELETE':
                    permission().delete(self, *args, **kwargs)
        # except TypeError:
        #     raise Exception(
        #         'some permission is not valid, maybe forget return true.')

    def get(self, pk, *args, **kwargs):
        '获取资源列表或资源'
        self.extends_class = {}
        self.permission_layer(pk)
        if pk is not None:
            query = self.db_session.query(
                self.object).filter(text(self.opk + '=' + "'" + pk + "'"))
        else:
            query = self.db_session.query(self.object)
        for arg in self.args_filter.args:
            a = request.args.get(arg, None)
            if a:
                args.run_arg(a)
        return query, 'sqlalchemy'
    def post_hook_before_create_object(self, data):
        """the program hook,remind to handle data before it created, do not recomand to use"""
        return data

    def post(self, *args, **kwargs):
        '新建该资源'
        # 获取request的json并新建一个用户
        self.permission_layer()
        class_dict = serializer.attr_dict_from_sqlalchemy(self)
        if not self.data:
            data = request.get_json()
        miss_keys = [key for key in class_dict if key not in data]
        if miss_keys:
            return 'you miss thoese keys {}'.format(','.join(miss_keys)), 'basic'
        data = self.post_hook_before_create_object(data)
        obj = self.create_object(json=data)
        self.db_session.add(obj)
        self.db_session.commit()
        self.broadcast.send('{}_on_value_seted'.format(
            self.object.__name__), self)
        return obj, 'sqlalchemy'

    def delete(self, pk, *args, **kwargs):
        '删除一个资源'
        self.permission_layer(pk)
        if self.real_delete:
            if pk is not None:
                self.db_session.query(self.object).filter(
                    text(self.opk + '=' + "'" + pk + "'")).delete(synchronize_session=False)
                self.db_session.commit()
                return self.db_session.query(self.object).filter(
                    text(self.opk + '=' + "'" + pk + "'")), 'sqlalchemy'
            else:
                return 'need pk', 'basic'
        else:
            if pk is not None:
                self.db_session.query(self.object).filter(
                    text(self.opk + '=' + "'" + pk + "'")).delete(synchronize_session=False)
                self.db_session().commit()
                self.db_session.query(self.object).filter(
                    text(self.opk + '=' + "'" + pk + "'")), 'sqlalchemy'
            else:
                return 'need pk', 'basic'

    def put(self, pk, *args, **kwargs):
        if pk:
            query = self.db_session.query(self.object).filter(text(
                self.opk + '=' + "'" + pk + "'"))
            instance = query.first()
            if instance:
                data_dict = serializer.attr_dict_from_sqlalchemy(instance)
                for key in data_dict:
                    setattr(self, key, getattr(instance, key))
                self.permission_layer(pk)
                if not self.data:
                    data = request.get_json()
                data_dict = serializer.attr_dict_from_sqlalchemy(instance)
                for key, value in data_dict.items():
                    data.update({key: value})
                    self.broadcast.send('{}_on_value_{}_updated'.format(
                        self.object.__name__, key), self, value)
                query.update(data, synchronize_session=False)
                self.db_session().commit()
                self.broadcast.send('{}all_value_updated'.format(
                    self.object.__name__), self)
                return self.db_session.query(self.object).filter(text(
                    self.opk + '=' + "'" + pk + "'")), 'sqlalchemy'
            else:
                return 'no such resource', 'basic'
        else:
            return 'need pk', 'basic'
