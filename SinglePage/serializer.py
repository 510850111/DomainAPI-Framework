# coding:utf-8
from datetime import datetime
from sqlalchemy.orm.query import Query
import copy


class Serializer():

    structures = {}
    # structures =
    # {
    #   User:
    #    {
    #      'name':'','gender':''
    #    },
    # }
    #
    update = True

    def get_structure(self, instance):
        self.update = True
        structure = self.dump(instance, self.class_type)
        self.update = False
        return structure

    def register_structure(self, instance, extends=None):
        _type = type(instance)
        self.structures.update({_type: self.get_structure(instance)})
        if extends:
            for key, value in extends.items():
                self.structures[_type].update(
                    {key: None})
                self.structures.update({
                    type(value): self.get_structure(value)})

    def dump(self, origin_instance, class_type='sqlalchemy'):
        # class_type choice 'sqlalchemy', 'basic'
        self.class_type = class_type
        if self.class_type == 'sqlalchemy':
            if isinstance(origin_instance, Query):
                origin_instance = origin_instance.all()
            return self.typping(origin_instance)
        elif self.class_type == 'basic':
            return self.typping(origin_instance)

    def cycling(self, instance):

        if isinstance(instance, (set, list)):
            m_list = []
            for item in instance:
                value = self.typping(item)
                m_list.append(value)
            return m_list
        if isinstance(instance, dict):
            m_dict = {}
            for item in instance:
                value = self.typping(instance[item])
                m_dict.update({item: value})
            return m_dict

    def typping(self, instance):

        if isinstance(instance, set):
            return self.cycling(instance)
        elif isinstance(instance, list):
            return self.cycling(instance)
        elif isinstance(instance, dict):
            return self.cycling(instance)
        elif isinstance(instance, (float, int, str, bytes, bool)):
            return instance
        elif isinstance(instance, datetime):
            return instance
        elif instance is None:
            return None
        else:
            return self.typping(self.mapping(instance))

    def mapping(self, instance):
        # _type = type(instance)
        # structure = self.structures.get(_type)
        # 惊天BUG，此处序列化器进入对象字典生成阶段，方式是判断，序列化字典是否为空
        # 如果为空，则使用attr生成字典，这会导致一个问题：
        # 如果，用户将对象所有内容都放入exclude列表，那么，这里的struct永远为空！
        # 解决方案，在此处判断是否为None而不是直接判断对象，因为{}在python中会被判断为None，但是使用is 来判断可以避免这个问题。
        # 在mapping_by_structure中再判断structure是否是空。
        if not self.update:
            return self.mapping_by_structure(instance)
        if self.class_type == 'basic':
            return self.attr_dict_from_basic(instance)
        elif self.class_type == 'sqlalchemy':
            return self.attr_dict_from_sqlalchemy(instance)

    def mapping_by_structure(self, origin_instance):
        _type = type(origin_instance)
        structure = self.structures.get(_type, None)
        response = copy.copy(structure)
        if structure is not None:
            for s in structure:
                value = getattr(origin_instance, s, None)
                response.update({s: value})
        return response

    def attr_dict_from_basic(self, instance):
        try:
            exclude = [e for e in instance.__exclude__]
        except:
            exclude = []
        full = dict([[e, getattr(instance, e)] for e in dir(instance)
                     if not e.startswith('_') and not
                     hasattr(getattr(instance, e),
                             '__call__') and e not in exclude])
        propery = dict([[p, getattr(instance,
                                    e).__get__(instance, type(instance))]
                        for p in full if hasattr(full[p], 'fset')])
        full.update(propery)
        return full

    def attr_dict_from_sqlalchemy(self, instance):
        try:
            exclude = [e for e in instance.__exclude__]
        except:
            exclude = []
        full = dict([[e, getattr(instance, e, None)]
                     for e in instance.__mapper__.c.keys()
                     if e not in exclude])
        return full

serializer = Serializer()
