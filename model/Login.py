# coding: utf-8
from SinglePage.general_view_with_sqlalchemy import GeneralViewWithSQLAlchemy
from sqlalchemy import Column, Integer, String
from model.Base import Base, db_session


class Login(GeneralViewWithSQLAlchemy, Base):
    """
        V1.0:
            登陆接口，传入openid和pwd后获得的base作为其它接口的验证凭据
            该接口同时具有，identify+pwd登陆，login记录，oauth code生成三种功能。
            该接口的openid，即大多数系统中的identifer，取名叫openid原因在于该字段实际上是使用
            请将获得的user_id和base放在header中
            格式XXX-user-id:1, XXX-base:xxx
    """
    db_session = db_session
    __tablename__ = 'Login'
    id = Column(Integer, primary_key=True)
    telephone = Column(String(15))
    user_id = Column(Integer)
    openid = Column(String(125), nullable=False)
    base = Column(String(400))
    login_time = Column(String(20))
    pwd = Column(String(125))
    opk = 'base'
