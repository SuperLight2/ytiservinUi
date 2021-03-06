__author__ = 'gumerovif'

import json
from time import time

from core.db_runner import DBRunner
from core.id_generator import IDGenerator
from core.u_types import UTypes
from core.u_vertex_types.vertex_types import UVertexTypes
from core.u_edge_types.edge_types import UEdgeTypes


class UGraphStorage(object):
    DBVertexesTable = 'u_vertices'
    DBEdgesTable = 'u_edges'

    @classmethod
    def _generate_new_id(cls, u_vertex_type_id):
        u_vertex_type = UTypes.get_vertex_type(u_vertex_type_id)
        # TODO(igumerov): use u_vertex_type_id!
        return IDGenerator.generate_unique_id()

    @classmethod
    def _get_vertex_type_id_by_uid(cls, uid):
        # TODO: check do we really need this function
        query = "SELECT utype FROM %s WHERE uid=%d" % (cls.DBVertexesTable, uid)
        result = DBRunner().run(query).get_only_or_none_result()
        return result.get('utype')

    @classmethod
    def vertex_create(cls, u_type_id):
        uid = cls._generate_new_id(u_type_id)
        query = "INSERT INTO %s (`uid`, `utype`, `deleted`, `data`) VALUE (%d, %d, 0, '%s')" \
                % (cls.DBVertexesTable, uid, u_type_id, json.dumps({}))
        return uid if DBRunner().run(query).get_number_of_affected_rows() == 1 else None

    @classmethod
    def vertex_get(cls, uid):
        query = "SELECT uid, utype, data FROM %s WHERE uid=%d AND deleted=0" % (cls.DBVertexesTable, uid)
        row = DBRunner().run(query).get_next()
        if row is None:
            return None
        uid = int(row["uid"])
        u_type_id = int(row["utype"])
        attrs = UTypes.get_vertex_type(u_type_id).get_data_attributes()
        result = {}.fromkeys(attrs)
        result.update({"uid": uid, "utype": u_type_id})
        result.update(json.loads(row["data"]))
        return result

    @classmethod
    def vertex_gets(cls, *args):
        result = dict()
        for uid in args:
            result[uid] = cls.vertex_get(uid)
        return result

    @classmethod
    def vertex_set(cls, uid, **kwargs):
        vertex = cls.vertex_get(uid)
        if vertex is None:
            raise BaseException("Unknown uid: " + uid)
        u_type_id = vertex['utype']
        u_vertex_type = UTypes.get_vertex_type(u_type_id)
        u_vertex_type.check_value(**kwargs)
        data = {}
        for attr_name in u_vertex_type.get_data_attributes():
            data[attr_name] = kwargs.get(attr_name, vertex.get(attr_name))
        query = "UPDATE %s SET data='%s' WHERE uid=%d AND deleted=0" % (cls.DBVertexesTable, json.dumps(data), uid)
        return DBRunner().run(query).get_number_of_affected_rows() == 1

    @classmethod
    def vertex_delete(cls, uid):
        query = "UPDATE %s SET deleted=1 WHERE uid=%d AND deleted=0" % (cls.DBVertexesTable, uid)
        return DBRunner().run(query).get_number_of_affected_rows() == 1

    @classmethod
    def edge_add(cls, uid1, uid2, u_type_id, info=''):
        if uid1 == uid2:
            raise BaseException("Self-loops are not permitted")
        u_type = UTypes.get_edge_type(u_type_id)
        attrs = u_type.get_const_attributes()
        uid1_type_id = cls._get_vertex_type_id_by_uid(uid1)
        uid2_type_id = cls._get_vertex_type_id_by_uid(uid2)
        if attrs['uid1_type'] != uid1_type_id:
            raise BaseException("Wrong type for vertex with uid:" + uid1)
        if attrs['uid2_type'] != uid2_type_id:
            raise BaseException("Wrong type for vertex with uid:" + uid2)

        timestamp = int(100 * time())
        queries = [
            "REPLACE INTO %s (`uid1`, `uid2`, `utype`, `deleted`, `info`, `timestamp`) "
            "VALUE (%d, %d, %d, 0, '%s', %d)"
            % (cls.DBEdgesTable, uid1, uid2, u_type_id, info, timestamp)
        ]

        u_inverse_type_id = attrs['inverse_type']
        if u_inverse_type_id is not None:
            u_inverse_type = UTypes.get_edge_type(u_inverse_type_id)
            inverse_attrs = u_inverse_type.get_const_attributes()
            if inverse_attrs['inverse_type'] != u_type_id:
                raise BaseException("Inconsistent exception. Check edges with utypes: %d, %d."
                                    % (u_type_id, u_inverse_type_id))
            if inverse_attrs['uid2_type'] != uid1_type_id:
                raise BaseException("Wrong type for vertex with uid:" + uid1)
            if inverse_attrs['uid1_type'] != uid2_type_id:
                raise BaseException("Wrong type for vertex with uid:" + uid2)
            queries.append(
                "REPLACE INTO %s (`uid1`, `uid2`, `utype`, `deleted`, `info`, `timestamp`) "
                "VALUE (%d, %d, %d, 0, '%s', %d)"
                % (cls.DBEdgesTable, uid2, uid1, u_inverse_type_id, info, timestamp)
            )
        return DBRunner().run_full_transaction(queries).was_success()

    @classmethod
    def edge_delete(cls, uid1, uid2, u_type_id):
        queries = [
            "UPDATE %s SET deleted=1 WHERE uid1=%d AND uid2=%d AND utype=%d AND deleted=0"
            % (cls.DBEdgesTable, uid1, uid2, u_type_id)
        ]
        u_type = UTypes.get_edge_type(u_type_id)
        attrs = u_type.get_const_attributes()
        u_inverse_type_id = attrs['inverse_type']
        if u_inverse_type_id is not None:
            queries.append(
                "UPDATE %s SET deleted=1 WHERE uid2=%d AND uid1=%d AND utype=%d AND deleted=0"
                % (cls.DBEdgesTable, uid1, uid2, u_inverse_type_id)
            )
        return DBRunner().run_full_transaction(queries).was_success()

    @classmethod
    def edge_get(cls, uid1, uid2, u_type):
        return DBRunner().run(
            "SELECT info, timestamp FROM %s WHERE uid1=%d AND uid2=%d AND utype=%d AND deleted=0"
            % (cls.DBEdgesTable, uid1, uid2, u_type)
        ).get_only_or_none_result()

    @classmethod
    def get_edges_by_type(cls, uid, u_type, limit=10):
        db = DBRunner().run(
            "SELECT uid2, info, timestamp FROM %s WHERE uid1=%d AND utype=%d AND deleted=0 "
            "ORDER BY timestamp DESC LIMIT %d"
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
            "SELECT COUNT(*) AS count FROM %s WHERE uid1=%d AND utype=%d AND deleted=0"
            % (cls.DBEdgesTable, uid, u_type))
        return result.get_only_result()["count"]

    @classmethod
    def can_delete_vertex(cls, uid):
        #TODO: should use async methods here
        results1 = DBRunner().run("SELECT 1 FROM %s WHERE uid1=%d AND deleted=0 LIMIT 1" % (cls.DBEdgesTable, uid))
        results2 = DBRunner().run("SELECT 1 FROM %s WHERE uid2=%d AND deleted=0 LIMIT 1" % (cls.DBEdgesTable, uid))
        return (results1.get_results_count() == 0) and (results2.get_results_count() == 0)


def load_graph():
    rows = DBRunner().run("SELECT uid FROM %s" % UGraphStorage.DBVertexesTable)
    while True:
        x = rows.get_next()
        if x is None:
            break
        IDGenerator.add_id(int(x['uid']))


if __name__ == '__main__':
    load_graph()

    user_id = UGraphStorage.vertex_create(UVertexTypes.USER)
    UGraphStorage.vertex_set(user_id, lastname="Bazarov", firstname="Ivan")
    user = UGraphStorage.vertex_get(user_id)
    assert (user['lastname'] == "Bazarov")
    assert (user['firstname'] == "Ivan")

    user2_id = UGraphStorage.vertex_create(UVertexTypes.USER)
    try:
        UGraphStorage.vertex_set(user2_id, lastname=1111)
    except BaseException, e:
        print "Expected behaviour: ", e
    UGraphStorage.vertex_set(user2_id, lastname="Yakimov", firstname="Constant")

    group_id = UGraphStorage.vertex_create(UVertexTypes.GROUP)
    UGraphStorage.vertex_set(group_id, name="FILMFILMFILM")

    user2_and_group = UGraphStorage.vertex_gets(user2_id, group_id)

    user2 = user2_and_group[user2_id]
    assert (user2['lastname'] == "Yakimov")
    assert (user2['firstname'] == "Constant")

    group = user2_and_group[group_id]
    assert (group['name'] == "FILMFILMFILM")

    resource_id = UGraphStorage.vertex_create(UVertexTypes.RESOURCE)
    UGraphStorage.vertex_set(resource_id, name="Gold")
    resource = UGraphStorage.vertex_get(resource_id)
    assert (resource['name'] == "Gold")

    print "UserID:", user_id
    print "User2ID:", user2_id
    print "GroupID:", group_id
    print "ResourceID:", resource_id

    UGraphStorage.edge_add(user_id, user2_id, UEdgeTypes.FRIENDS)
    assert(UGraphStorage.edge_get(user_id, user2_id, UEdgeTypes.FRIENDS) is not None)
    assert(UGraphStorage.edge_get(user2_id, user_id, UEdgeTypes.FRIENDS) is not None)

    UGraphStorage.edge_add(user_id, group_id, UEdgeTypes.MEMBER_OF_GROUP)
    assert(UGraphStorage.edge_get(user_id, group_id, UEdgeTypes.MEMBER_OF_GROUP) is not None)
    assert(UGraphStorage.get_edges_count(user_id, UEdgeTypes.MEMBER_OF_GROUP) == 1)

    UGraphStorage.edge_add(user_id, resource_id, UEdgeTypes.LIKE)
    assert(UGraphStorage.edge_get(user_id, resource_id, UEdgeTypes.LIKE) is not None)
    assert(UGraphStorage.edge_get(resource_id, user_id, UEdgeTypes.LIKED_BY) is not None)

    edges = UGraphStorage.get_edges_by_type(user_id, UEdgeTypes.MEMBER_OF_GROUP)
    assert(len(edges) == 1)
    assert (edges[0]['uid2'] == group_id)
    assert(not UGraphStorage.can_delete_vertex(user_id))
    assert(not UGraphStorage.can_delete_vertex(group_id))

    UGraphStorage.edge_delete(user_id, group_id, UEdgeTypes.MEMBER_OF_GROUP)
    UGraphStorage.edge_delete(user_id, user2_id, UEdgeTypes.FRIENDS)
    UGraphStorage.edge_delete(user_id, resource_id, UEdgeTypes.LIKE)
    assert(UGraphStorage.edge_get(user_id, group_id, UEdgeTypes.MEMBER_OF_GROUP) is None)
    assert(UGraphStorage.edge_get(user_id, user2_id, UEdgeTypes.FRIENDS) is None)
    assert(UGraphStorage.edge_get(user2_id, user_id, UEdgeTypes.FRIENDS) is None)
    assert(UGraphStorage.can_delete_vertex(user_id))
    assert(UGraphStorage.can_delete_vertex(group_id))

    UGraphStorage.edge_add(user_id, user2_id, UEdgeTypes.FRIENDS)
    assert(UGraphStorage.edge_get(user_id, user2_id, UEdgeTypes.FRIENDS) is not None)
    assert(UGraphStorage.edge_get(user2_id, user_id, UEdgeTypes.FRIENDS) is not None)

    UGraphStorage.edge_delete(user_id, user2_id, UEdgeTypes.FRIENDS)
    assert(UGraphStorage.edge_get(user_id, user2_id, UEdgeTypes.FRIENDS) is None)
    assert(UGraphStorage.edge_get(user2_id, user_id, UEdgeTypes.FRIENDS) is None)
    assert(UGraphStorage.can_delete_vertex(user_id))

    UGraphStorage.vertex_delete(user_id)
    UGraphStorage.vertex_delete(group_id)
    assert(UGraphStorage.vertex_get(user_id) is None)
    assert(UGraphStorage.vertex_get(group_id) is None)
    print "Tests OK!"