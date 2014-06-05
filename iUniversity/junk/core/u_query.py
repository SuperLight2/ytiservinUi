__author__ = 'gumerovif'


class UQuery(object):
    def __init__(self):
        self.description = []

    def add(self, action, **kwargs):
        self.description.append((action, kwargs))
        return self

    @classmethod
    def u_vertex_create(cls, u_type):
        return UQuery().add('create_vertex', {'type': u_type})

    @classmethod
    def u_vertex_edit(cls, uid, key, value):
        return UQuery().add('edit_vertex', {'uid': uid, 'key': key, 'value': value})

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
