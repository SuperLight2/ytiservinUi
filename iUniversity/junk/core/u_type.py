__author__ = 'gumerovif'

from core.u_field import UField


class UType(object):
    uid = UField(field_type=int, prefix="")
    utype = UField(field_type=int, prefix="")

    @classmethod
    def _get_all_attributes(cls):
        for pcls in cls.__mro__:
            if pcls is object:
                continue
            for attr_name, attr in pcls.__dict__.iteritems():
                yield attr_name, attr

    @classmethod
    def get_attributes(cls, prefix=""):
        result = {}
        for attr_name, attr in cls._get_all_attributes():
            if not isinstance(attr, UField):
                continue
            if attr.prefix == prefix:
                result[attr_name] = attr
        return result


class UVertexType(UType):
    pass


class UEdgeType(UType):
    uid1_type = None
    uid2_type = None
    const_direction = None
    const_inverse_type = None

    uid1 = UField(field_type=int, prefix="")
    uid2 = UField(field_type=int, prefix="")
    timestamp = UField(field_type=int, prefix="")
    info = UField(field_type=str, prefix="")