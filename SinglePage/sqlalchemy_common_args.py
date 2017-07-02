from sqlalchemy import text, desc
from sqlalchemy.orm import joinedload, load_only, subqueryload, lazyload


def filter(query, value, instance):
    return query.filter(text(value))


def asc_order_by(query, value, instance):
    return query.order_by(text(value))


def desc_order_by(query, value, instance):
    return query.order_by(desc(text(value)))


def limit(query, value, instance):
    return query.limit(value)


def offset(query, value, instance):
    offset = int(value)
    if offset > 0:
        return query.offset(offset - 1)
    else:
        return query


def includes(query, value, instance):
    key = value.split(',')
    for k in key:
        try:
            extends_resources = app.config['resources'][k]
        except KeyError:
            abort(406)
        # TODO
        extends_resources().set_permission(self.permission)
        passed, permission, memo, status_code = extends_resources()\
            .get_permission_passed(None)
        if passed:
            self.extends_class.update({k: extends_resources()})
            # what's the diffrence bewtten subqueryload and joinedload?
            query = query.join(extends_resources)
            query = query.options(joinedload(k))
        else:
            abort(status_code)
    return query


def fileds(query, value, instance):
    vs = value.split(',')
    exclude = self.__exclude__
    self.set_exclude([])
    members = serializer.dump(self)
    self.set_exclude([e for e in members if e not in vs] + list(exclude))
    for v in vs:
        query.options(load_only(v))
    return query

sqlalchemuy_common_args_list = [
    {'includes': includes},
    {'filter': filter},
    {'asc_order_by': asc_order_by},
    {'desc_order_by': desc_order_by},
    {'fileds': fileds},
    {'offset': offset},
    {'limit': limit},
]
