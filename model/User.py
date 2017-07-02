# coding:utf-8
import uuid
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean
from SinglePage.singlepage import request
from model.Base import Base, db_session
from SinglePage.general_view_with_sqlalchemy import GeneralViewWithSQLAlchemy


class User(GeneralViewWithSQLAlchemy, Base):
    """
        V1.0:
            用户资源，创建时需要pwd会被hashed，这会花费一定时间
        V2.0:
            新增和镖师、管理者、镖单、用户账户关联
    """
    db_session = db_session
    real_delete = False

    class SEX_CHOICE():
        FEMALE = 'female'
        MALE = 'male'
        UNKNOWN = 'unknown'

    __tablename__ = 'User'
    # model

    id = Column(Integer, primary_key=True)
    telephone = Column(String(15), unique=True)
    create_time = Column(String(20))
    nickname = Column(String(20))
    baned = Column(Boolean, default=False)
    sex = Column('sex', Enum(SEX_CHOICE.FEMALE,
                             SEX_CHOICE.MALE, SEX_CHOICE.UNKNOWN))
    img_url = Column(String(5000))
    openid = Column(String(125), unique=True, nullable=False)
    password = Column(String(400))
    permissions = Column(String(20))

