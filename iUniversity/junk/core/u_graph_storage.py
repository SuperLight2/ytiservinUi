__author__ = 'gumerovif'

import json
from time import time

from core.db_runner import DBRunner
from core.id_generator import IDGenerator
from core.u_field import UField
from core.u_types import UTypes
from core.u_vertex_types.u_vertex_types import UVertexTypes
from core.u_edge_types.u_edge_types import UEdgeTypes
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
    def u_vertex_create(cls, u_type_id):
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
    def u_vertex_get(cls, uid):
        query = "SELECT utype, data FROM %s WHERE uid=%d" % (cls.DBVertexesTable, uid)
        row = DBRunner().run(query).get_only_or_none_result()
        if row is None:
            return None
        result = {
            "uid": uid,
            "utype": int(row["utype"]),
        }
        result.update(json.loads(row["data"]))
        return result

    @classmethod
    def u_vertex_set(cls, uid, key, value):
        vertex = cls.u_vertex_get(uid)
        if vertex is None:
            raise BaseException("Unknown uid: " + uid)
        if key not in vertex:
            raise BaseException("Unknown key: " + key)

        u_type_id = cls.get_vertex_type_id_by_id(uid)
        u_vertex_type = UTypes.get(u_type_id)
        if not issubclass(u_vertex_type, UVertexType):
            raise BaseException("Never happens!")
        data = {}
        for ckey, field in u_vertex_type.get_attributes(UField.DATA).iteritems():
            value_type = field.field_type
            if (ckey == key) and (not isinstance(value, value_type)):
                raise BaseException("Wrong value type for key: " + key + ". Need: " + value_type + ". Given: " + type(value))
            data[ckey] = vertex[ckey]
        data[key] = value
        data_json = json.dumps(data)
        query = "UPDATE %s SET data='%s' WHERE uid=%d" % (cls.DBVertexesTable, data_json, uid)
        return DBRunner().run(query).was_success()


    @classmethod
    def u_vertex_delete(cls, uid):
        query = "DELETE FROM %s WHERE uid=%d" % (cls.DBVertexesTable, uid)
        return DBRunner().run(query).get_number_of_affected_rows() == 1


    @classmethod
    def u_edge_add(cls, uid1, uid2, u_type_id, info=''):
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
    def u_edge_delete(cls, uid1, uid2, u_type_id):
        return DBRunner().run(
            "DELETE FROM %s WHERE uid1=%d AND uid2=%d AND utype=%d" % (cls.DBEdgesTable, uid1, uid2, u_type_id)
        ).get_number_of_affected_rows() == 1

    @classmethod
    def u_edge_get(cls, uid1, uid2, u_type):
        return DBRunner().run(
            "SELECT info, timestamp FROM %s WHERE uid1=%d AND uid2=%d AND utype=%d"
            % (cls.DBEdgesTable, uid1, uid2, u_type)
        ).get_only_or_none_result()

    @classmethod
    def u_get_edges_by_type(cls, uid, u_type, limit=10):
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
    def u_get_edges_count(cls, uid, u_type):
        result = DBRunner().run(
            "SELECT COUNT(*) AS count FROM %s WHERE uid1=%d AND utype=%d" % (cls.DBEdgesTable, uid, u_type))
        return result.get_only_result()["count"]


if __name__ == '__main__':
    # TODO: impl multiget
    # TODO: set data to vertex function should be able to deal with dictionaries
    # TODO: specify graph operations
    user_id = UGraphStorage.u_vertex_create(UVertexTypes.USER)
    UGraphStorage.u_vertex_set(user_id, "lastname", "Bazarov")
    UGraphStorage.u_vertex_set(user_id, "firstname", "Ivan")

    group_id = UGraphStorage.u_vertex_create(UVertexTypes.GROUP)
    UGraphStorage.u_vertex_set(group_id, "name", "FILMFILMFILM!!!")

    print user_id, group_id
    print UGraphStorage.u_vertex_get(user_id)
    print UGraphStorage.u_vertex_get(group_id)
    print UGraphStorage.u_edge_add(user_id, group_id, UEdgeTypes.MEMBER_OF_GROUP)
    #UGraphStorage.u_vertex_delete(user_id)
    #UGraphStorage.u_vertex_delete(group_id)
