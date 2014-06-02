__author__ = 'gumerovif'

from id_generator import IDGenerator


class ObjectType:
    USER = 1 # or maybe it would be better to replace the numbers with an object constructors?
    GROUP = 2
    RESOURCE = 3


class GS(object):
    _uid_to_object_type = dict()
    _storage = dict()

    @classmethod
    def get_object_type(cls, uid):
        return cls._uid_to_object_type[uid]

    @classmethod
    def get_object(cls, uid):
        object_type = cls.get_object_type(uid)
        return cls._storage[object_type][uid]

    @classmethod
    def set_object_type(cls, uid, object_type):
        cls._uid_to_object_type[uid] = object_type

    @classmethod # we should use this function when creating a new objects
    def generate_new_id(cls, object_type):
        uid = IDGenerator.generate_unique_id()
        cls.set_object_type(uid, object_type)
        return uid

    @classmethod
    def set(cls, uid, some_object):
        object_type = cls.get_object_type(uid)
        cls._storage[object_type][uid] = some_object

class A:
    d = dict()

    @classmethod
    def get(cls):
        cls.d[5] = 1
        return cls.d[5]

if __name__ == '__main__':
    a = A()
    print a.d
    a.get() = 2
    print a.d
    x = 2
    print a.d