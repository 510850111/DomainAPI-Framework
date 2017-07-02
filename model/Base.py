# coding: utf-8
import sys
sys.path.append('..')

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# from model.init_data import init_data
# hosts = '/etc/hosts'


# def db():
#     with open(hosts, 'r') as f:
#         for line in f:
#             print(line)
#     return '8df361d394db'
# db = db()


# engine = create_engine('mysql+pymysql://root:TaylorHere357753@dab/escort?charset=utf8')
engine = create_engine('sqlite:///escort.db', convert_unicode=True, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
