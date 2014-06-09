__author__ = 'gumerovif'

import json

from core.db_runner import DBRunner
from core.id_generator import IDGenerator
from core.u_field import UField
from core.u_types import UTypes
from core.u_vertex_types.u_vertex_types import UVertexTypes
from core.u_edge_types.u_edge_types import UEdgeTypes
from core.u_type import UVertexType, UEdgeType


class UGraphStorage(object):
    _id_to_type = dict()
    DBVertexesTable = 'u_vertexes'
    DBEdgesTable = 'u_edges'

    @classmethod
    def generate_new_id(cls, u_vertex_type_id):
        u_vertex_type = UTypes.get(u_vertex_type_id)
        if u_vertex_type is None:
            raise BaseException("unknown type index: %d" % u_vertex_type_id)
        if not issubclass(u_vertex_type, UVertexType):
            raise BaseException(str(u_vertex_type) + " is not a UVertexType class")
        uid = IDGenerator.generate_unique_id()
        cls._id_to_type[uid] = u_vertex_type_id
        return uid

    @classmethod
    def get_vertex_type_id_by_id(cls, uid):
        return cls._id_to_type.get(uid, None)

    @classmethod
    def u_vertex_create(cls, u_type_id):
        u_vertex_type = UTypes.get(u_type_id)
        if issubclass(u_vertex_type, UVertexType):
            uid = cls.generate_new_id(u_type_id)
            data = {}
            for key, field in u_vertex_type.get_attributes(UField.DATA).iteritems():
                data[key] = field.field_type()
            data_json = json.dumps(data)
            query = "INSERT INTO %s VALUE (%d, %d, '%s')" % (cls.DBVertexesTable, uid, u_type_id, data_json)
            db = DBRunner().run(query)
            if not db.was_success():
                raise BaseException(db.get_error_message())
            return uid
        else:
            raise BaseException(str(u_vertex_type) + " is not a UVertexType class")

    @classmethod
    def u_vertex_get(cls, uid):
        query = "SELECT id, u_type, data FROM %s WHERE id=%d" % (cls.DBVertexesTable, uid)
        results = DBRunner().run(query)
        if not results.was_success():
            raise BaseException(results.get_error_message())
        if results.get_results_count() == 0:
            return None
        row = results.get_only_result()
        result = {
            "uid": uid,
            "utype": int(row["u_type"]),
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
        if issubclass(u_vertex_type, UVertexType):
            data = {}
            for ckey, field in u_vertex_type.get_attributes(UField.DATA).iteritems():
                value_type = field.field_type
                if (ckey == key) and (not isinstance(value, value_type)):
                    raise BaseException("Wrong value type for key: " + key + ". Need: " + value_type + ". Given: " + type(value))
                data[ckey] = vertex[ckey]
            data[key] = value
            data_json = json.dumps(data)
            query = "UPDATE %s SET data='%s' WHERE id=%d" % (cls.DBVertexesTable, data_json, uid)
            return DBRunner().run(query).was_success()
        else:
            raise BaseException("Never happens!")

    @classmethod
    def u_vertex_delete(cls, uid):
        query = "DELETE FROM %s WHERE id=%d" % (cls.DBVertexesTable, uid)
        return DBRunner().run(query).was_success()


    @classmethod
    def u_edge_add(cls, uid1, uid2, u_type):
        return UQuery().add('create_edge', {'uid1': uid1, 'uid2': uid2, 'type': u_type, 'info': ''})

    @classmethod
    def u_edge_delete(cls, uid1, uid2, u_type):
        return UQuery().add('delete_edge', {'uid1': uid1, 'uid2': uid2, 'type': u_type})

    @classmethod
    def u_edge_get(cls, uid1, uid2, u_type):
        return UQuery().add('get_edge', {'uid1': uid1, 'uid2': uid2, 'type': u_type})

    @classmethod
    def u_get_edges_by_type(cls, uid, u_type):
        return UQuery().add('get_edges', {'uid': uid, 'type': u_type})

    @classmethod
    def u_get_edges_count(cls, uid, u_type):
        return UQuery().add('get_edges_count', {'uid': uid, 'type': u_type})


if __name__ == '__main__':
    uid = UGraphStorage.u_vertex_create(UVertexTypes.USER)
    print uid
    print UGraphStorage.u_vertex_set(uid, "lastname", "Bazarov")
    print UGraphStorage.u_vertex_set(uid, "firstname", "Ivan")
    print UGraphStorage.u_vertex_get(uid)
    print UGraphStorage.u_vertex_delete(uid)
