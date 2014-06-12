__author__ = 'gumerovif'

import json
from time import time

from core.db_runner import DBRunner
from core.id_generator import IDGenerator
from core.u_field import UField
from core.u_types import UTypes
from core.u_vertex_types.vertex_types import UVertexTypes
from core.u_edge_types.edge_types import UEdgeTypes
from core.u_type import UVertexType, UEdgeType


class UGraphStorage(object):
    DBVertexesTable = 'u_vertices'
    DBEdgesTable = 'u_edges'

    @classmethod
    def generate_new_id(cls, u_vertex_type_id):
        u_vertex_type = UTypes.get(u_vertex_type_id)
        if u_vertex_type is None:
            raise BaseException("unknown type index: %d" % u_vertex_type_id)
        if not issubclass(u_vertex_type, UVertexType):
            raise BaseException(str(u_vertex_type) + " is not a UVertexType class")
        # TODO(igumerov): use u_vertex_type_id!
        return IDGenerator.generate_unique_id()

    @classmethod
    def get_vertex_type_id_by_id(cls, uid):
        query = "SELECT utype FROM %s WHERE uid=%d" % (cls.DBVertexesTable, uid)
        result = DBRunner().run(query).get_only_or_none_result()
        if result is None:
            return None
        return result["utype"]

    @classmethod
    def vertex_create(cls, u_type_id):
        u_vertex_type = UTypes.get(u_type_id)
        if issubclass(u_vertex_type, UVertexType):
            uid = cls.generate_new_id(u_type_id)
            data = {}
            for key, field in u_vertex_type.get_attributes(UField.DATA).iteritems():
                data[key] = field.field_type()
            data_json = json.dumps(data)
            query = "INSERT INTO %s (`uid`, `utype`, `data`) VALUE (%d, %d, '%s')" \
                    % (cls.DBVertexesTable, uid, u_type_id, data_json)
            DBRunner().run(query)
            return uid
        else:
            raise BaseException(str(u_vertex_type) + " is not a UVertexType class")

    @classmethod
    def vertex_get(cls, *args): #args should be a list of uids
        if len(args) == 1:
            query = "SELECT uid, utype, data FROM %s WHERE uid=%d" % (cls.DBVertexesTable, args[0])
        else:
            uids = ", ".join(map(str, args))
            query = "SELECT uid, utype, data FROM %s WHERE uid IN (%s)" % (cls.DBVertexesTable, uids)
        rows = DBRunner().run(query)
        result = {}.fromkeys(args)
        while True:
            row = rows.get_next()
            if row is None:
                break
            uid = int(row['uid'])
            result[uid] = {
                "uid": uid,
                "utype": int(row["utype"]),
            }
            result[uid].update(json.loads(row["data"]))
        if len(args) == 1:
            result = result[args[0]]
        return result

    @classmethod
    def vertex_set(cls, uid, **kwargs):
        vertex = cls.vertex_get(uid)
        if vertex is None:
            raise BaseException("Unknown uid: " + uid)

        u_type_id = cls.get_vertex_type_id_by_id(uid)
        u_vertex_type = UTypes.get(u_type_id)
        if not issubclass(u_vertex_type, UVertexType):
            raise BaseException("Never happens!")
        data = {}
        for key, field in u_vertex_type.get_attributes(UField.DATA).iteritems():
            data[key] = vertex[key]
            if key in kwargs:
                new_value = kwargs.get(key)
                value_type = field.field_type
                if not isinstance(new_value, value_type):
                    raise BaseException(
                        "Wrong value type for key: " + key + ". Need: " + value_type + ". Got: " + type(new_value))
                data[key] = new_value
        query = "UPDATE %s SET data='%s' WHERE uid=%d" % (cls.DBVertexesTable, json.dumps(data), uid)
        DBRunner().run(query)

    @classmethod
    def vertex_delete(cls, uid):
        query = "DELETE FROM %s WHERE uid=%d" % (cls.DBVertexesTable, uid)
        return DBRunner().run(query).get_number_of_affected_rows() == 1

    @classmethod
    def edge_add(cls, uid1, uid2, u_type_id, info=''):
        u_type = UTypes.get(u_type_id)
        if issubclass(u_type, UEdgeType):
            attrs = u_type.get_attributes(UField.CONST)
            if attrs['uid1_type'].const_value != cls.get_vertex_type_id_by_id(uid1):
                raise BaseException("Wrong type for vertex with uid:" + uid1)
            if attrs['uid2_type'].const_value != cls.get_vertex_type_id_by_id(uid2):
                raise BaseException("Wrong type for vertex with uid:" + uid2)
            timestamp = int(100 * time())
            return DBRunner().run(
                "INSERT INTO %s (`uid1`, `uid2`, `utype`, `info`, `timestamp`) VALUE (%d, %d, %d, '%s', %d)"
                % (cls.DBEdgesTable, uid1, uid2, u_type_id, info, timestamp)).get_number_of_affected_rows()
        else:
            raise BaseException("Unknown edge type: " + u_type_id)

    @classmethod
    def edge_delete(cls, uid1, uid2, u_type_id):
        return DBRunner().run(
            "DELETE FROM %s WHERE uid1=%d AND uid2=%d AND utype=%d" % (cls.DBEdgesTable, uid1, uid2, u_type_id)
        ).get_number_of_affected_rows() == 1

    @classmethod
    def edge_get(cls, uid1, uid2, u_type):
        return DBRunner().run(
            "SELECT info, timestamp FROM %s WHERE uid1=%d AND uid2=%d AND utype=%d"
            % (cls.DBEdgesTable, uid1, uid2, u_type)
        ).get_only_or_none_result()

    @classmethod
    def get_edges_by_type(cls, uid, u_type, limit=10):
        db = DBRunner().run(
            "SELECT uid2, info, timestamp FROM %s WHERE uid1=%d AND utype=%d ORDER BY timestamp DESC LIMIT %d"
            % (cls.DBEdgesTable, uid, u_type, limit)
        )
        results = []
        for i in xrange(limit):
            x = db.get_next()
            if x is None:
                break
            results.append(x)
        return results

    @classmethod
    def get_edges_count(cls, uid, u_type):
        result = DBRunner().run(
            "SELECT COUNT(*) AS count FROM %s WHERE uid1=%d AND utype=%d" % (cls.DBEdgesTable, uid, u_type))
        return result.get_only_result()["count"]

    @classmethod
    def can_delete_vertex(cls, uid):
        results1 = DBRunner().run("SELECT 1 FROM %s WHERE uid1=%d LIMIT 1" % (cls.DBEdgesTable, uid))
        results2 = DBRunner().run("SELECT 1 FROM %s WHERE uid2=%d LIMIT 1" % (cls.DBEdgesTable, uid))
        return (results1.get_results_count() == 0) and (results2.get_results_count() == 0)


def load_graph(config_file):
    rows = DBRunner().run("SELECT uid FROM %s" % UGraphStorage.DBVertexesTable)
    while True:
        x = rows.get_next()
        if x is None:
            break
        IDGenerator.add_id(int(x['uid']))


if __name__ == '__main__':
    # TODO: impl can_delete_vertex
    # TODO: specify graph operations
    load_graph(None)

    user_id = UGraphStorage.vertex_create(UVertexTypes.USER)
    UGraphStorage.vertex_set(user_id, lastname="Bazarov", firstname="Ivan")

    group_id = UGraphStorage.vertex_create(UVertexTypes.GROUP)
    UGraphStorage.vertex_set(group_id, name="FILMFILMFILM!!!")

    print user_id, group_id
    print UGraphStorage.vertex_get(user_id)
    print UGraphStorage.vertex_get(group_id)
    print UGraphStorage.edge_add(user_id, group_id, UEdgeTypes.MEMBER_OF_GROUP)
    if (not UGraphStorage.can_delete_vertex(user_id)) or (not UGraphStorage.can_delete_vertex(group_id)):
        UGraphStorage.edge_delete(user_id, group_id, UEdgeTypes.MEMBER_OF_GROUP)
    UGraphStorage.vertex_delete(user_id)
    UGraphStorage.vertex_delete(user_id)