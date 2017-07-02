# coding:utf-8
import sys
import uuid
from SinglePage.singlepage import *
from sqlalchemy import *
from types import SimpleNamespace as Namespace
from SinglePage.general_view_with_sqlalchemy import GeneralViewWithSQLAlchemy
from model.Base import db_session, init_db, Base
from describer import Describer

dyp_apps = {}
column_types = dict([[name,getattr(sys.modules['__main__'],name)] for name in dir()])


def make_model(route_name, name, note):
    """
        the key of the system is the column made by the json
    """
    members = {
        'db_session':db_session,
        '__tablename__':name,
    }

    for filed in note.fileds:
        members.update({filed.column_name:make_column(filed)})
    
    dyp_apps.update({type(name, (GeneralViewWithSQLAlchemy, Base), members):"/%s/" % route_name})

def make_column(filed):
    #dynamic types come from namespace
    #dynamic keyword argments
    if filed.column_argments:
        return Column(column_types[filed.column_type], **filed.column_argments.__dict__)
    else:
        return Column(column_types[filed.column_type])

def make_a_route(route, data):
    route_path = [r.text for r in route]
    route_path.append(data.text)
    route_name = '/'.join(route_path)
    if "note" in dir(data):
        note = json.loads(data.note, object_hook=lambda d: Namespace(**d))
        make_model(route_name, data.text, note)

@app.teardown_request
def auto_rollback(exception):
    if exception:
        db_session.rollback()
        db_session.remove()
    db_session.remove()

if __name__ == '__main__':
    des = Describer('Gateway.km')
    des.traversal(des.tree.root, make_a_route)
    for obj in dyp_apps:
        print(obj)
        print(dyp_apps[obj])
        register(obj, dyp_apps[obj])
    init_db()
    app.run(host='0.0.0.0', debug=True, port=5050)
# # # # # # # # # # # start the engine# # # # # # # # # # # # # # # # # # #
