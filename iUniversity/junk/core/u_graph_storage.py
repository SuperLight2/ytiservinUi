__author__ = 'gumerovif'

import json

from core.id_generator import IDGenerator
from core.u_type import UVertexType, UEdgeType
from core.u_types import UVertexTypes, UEdgeTypes
from core.db_runner import DBRunner


class UGraphStorage(object):
    _id_to_type = dict()
    DBVertexesTable = 'u_vertexes'
    DBEdgesTable = 'u_edges'


    # we should use this function when creating a new objects
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
    def u_vertex_set(cls, uid, key, value):
        query = "SELECT data FROM %s WHERE id=%d" % (cls.DBVertexesTable, uid)
        results = DBRunner.run(query)
        print results

    @classmethod
    def u_vertex_delete(cls, uid):
        return UQuery().add('delete_vertex', {'uid': uid})

    @classmethod
    def u_vertex_get(cls, uid):
        return UQuery().add('get_vertex', {'uid': uid})

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
    #UGraphStorage.u_vertex_set(uid, "required_last_name", "IVAN")
