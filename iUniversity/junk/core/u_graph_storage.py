__author__ = 'gumerovif'

import json

from core.id_generator import IDGenerator
from core.u_types import UVertexTypes, UEdgeTypes
from core.db_runner import DBRunner


class UGraphStorage(object):
    _id_to_type = dict()
    DBVertexesTable = 'u_vertexes'
    DBEdgesTable = 'u_edges'

    @classmethod
    def generate_new_id(cls, u_vertex_type_id):
        if UVertexTypes.get(u_vertex_type_id) is None:
            raise BaseException("wrong vertex index %d" % u_vertex_type_id)
        uid = IDGenerator.generate_unique_id()
        cls._id_to_type[uid] = u_vertex_type_id
        return uid

    @classmethod
    def get_vertex_type_id_by_id(cls, id):
        return cls._id_to_type.get(id, None)

    @classmethod
    def u_vertex_create(cls, u_type_id):
        uid = cls.generate_new_id(u_type_id)
        data_json = json.dumps({})
        query = "INSERT INTO %s VALUE (%d, %d, '%s')" % (cls.DBVertexesTable, uid, u_type_id, data_json)
        DBRunner.run(query)
        return uid

    @classmethod
    def u_vertex_get(cls, uid):
        query = "SELECT * FROM %s WHERE id=%d" % (cls.DBVertexesTable, uid)
        results = DBRunner.run(query)
        if len(results) == 0:
            return None, None
        if len(results) != 0:
            result = results[0]
            return int(result["u_type"]), json.loads(result["data"])

    @classmethod
    def u_vertex_set(cls, uid, key, value):
        u_type, data = cls.u_vertex_get(uid)
        data[key] = value
        data = json.dumps(data)
        DBRunner.run("UPDATE %s SET data='%s' WHERE id=%d" % (cls.DBVertexesTable, data, uid))

    @classmethod
    def u_vertex_delete(cls, uid):
        query = "DELETE FROM %s WHERE id=%d" % (cls.DBVertexesTable, uid)
        DBRunner.run(query)


    @classmethod
    def u_vertex_get_type(cls, uid):
        return UQuery().add('get_vertex_type', {'uid': uid})

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
    print id
    UGraphStorage.u_vertex_set(uid, "required_last_name", "IVAN")
    u_type, data = UGraphStorage.u_vertex_get(uid)
    print u_type, data
    UGraphStorage.u_vertex_delete(uid)
