# coding:utf-8
import sys
import uuid
from SinglePage.singlepage import *
from sqlalchemy import *
from SinglePage.general_view_with_sqlalchemy import GeneralViewWithSQLAlchemy
from model.Base import db_session, init_db, Base
from model.Login import Login
from model.User import User

dyp_apps = {}

column_types = dict([[name,getattr(sys.modules['__main__'],name)] for name in dir()])
def make_model(name, note):
    """
        the key of the system is the column made by the json
    """
    members = {
        'db_session':db_session,
        '__tablename__':name,
        'id':make_column(note)
    }
    
    dyp_apps.update({type(name, (GeneralViewWithSQLAlchemy, Base), members):"/%s/" % name})

def make_column(note):
    #dynamic types come from namespace
    #dynamic keyword argments
    return Column(column_types[note.column_type], **note.keyword_argments)


@app.teardown_request
def auto_rollback(exception):
    if exception:
        db_session.rollback()
        db_session.remove()
    db_session.remove()

if __name__ == '__main__':
    class note():
        column_type = 'Integer'
        keyword_argments = {'primary_key':True}
    make_model('model',note())
    for obj in dyp_apps:
        register(obj, dyp_apps[obj])
    init_db()
    app.run(host='0.0.0.0', debug=True, port=5050)
# # # # # # # # # # # start the engine# # # # # # # # # # # # # # # # # # #
