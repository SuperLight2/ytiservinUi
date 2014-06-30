__author__ = 'gumerovif'

from core.u_field import UField


class UType(object):
    uid = UField.RequiredInteger()
    utype = UField.RequiredInteger()
    deleted = UField.RequiredInteger()

    @classmethod
    def _get_all_attributes(cls):
        for pcls in cls.__mro__:
            if pcls is object:
                continue
            for attr_name, attr in pcls.__dict__.iteritems():
                yield attr_name, attr

    @classmethod
    def _get_attributes(cls, prefix=""):
        result = {}
        for attr_name, attr in cls._get_all_attributes():
            if not isinstance(attr, UField):
                continue
            if attr.prefix == prefix:
                result[attr_name] = attr
        return result

    @classmethod
    def get_const_attributes(cls):
        return cls._get_attributes(UField.CONST)

    @classmethod
    def get_data_attributes(cls):
        return cls._get_attributes(UField.DATA)


class UVertexType(UType):
    @classmethod
    def get_data_template(cls):
        result = {}
        for key, field in cls.get_data_attributes().iteritems():
            value_type = field.get_field_type()
            result[key] = value_type()
        return result


class UEdgeType(UType):
    uid1_type = None
    uid2_type = None
    inverse_type = None

    uid1 = UField.RequiredInteger()
    uid2 = UField.RequiredInteger()
    timestamp = UField.RequiredInteger()
    info = UField.RequiredString()