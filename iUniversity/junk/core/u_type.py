__author__ = 'gumerovif'

from core.u_field import UField


class UType(object):
    _db_table_name = UField.Virtual()

    @classmethod
    def _get_all_attributes(cls):
        for pcls in cls.__mro__:
            if pcls is object:
                continue
            for attr_name, attr in pcls.__dict__.iteritems():
                if not isinstance(attr, UField):
                    continue
                yield attr_name, attr

    @classmethod
    def get_const_attributes(cls):
        result = dict()
        for attr_name, attr in cls._get_all_attributes():
            if attr.is_constant():
                result[attr_name] = attr.get_value()
        return result

    @classmethod
    def get_db_table_name(cls):
        return cls._db_table_name.get_value()

    """@classmethod
    def get_data_template(cls):
        result = {}
        for key, field in cls.get_data_attributes().iteritems():
            value_type = field.get_field_type()
            result[key] = value_type()
        return result"""

    def __init__(self, **kwargs):
        self.validate()

    def get_attribute_value(self, attr_name):
        pass

    def set_attribute_value(self, attr_name, value):
        pass

    def validate(self):
        for attr_name, attr in self._get_all_attributes():
            attr.validate()


class UVertexType(UType):
    UType._db_table_name = UField.Constant('u_vertices')

    uid = UField.RequiredInteger()
    utype = UField.RequiredShortInteger()
    deleted = UField.RequiredBoolean()


class UEdgeType(UType):
    UType._db_table_name = UField.Constant('u_edges')

    uid1_type = UField.Virtual()
    uid2_type = UField.Virtual()
    inverse_type = UField.Virtual()

    uid1 = UField.RequiredInteger()
    uid2 = UField.RequiredInteger()
    timestamp = UField.RequiredInteger()
    info = UField.RequiredString()
    deleted = UField.RequiredBoolean()


if __name__ == '__main__':
    UVertexType().validate()
    try:
        UEdgeType().validate()
    except BaseException, e:
        print e
    print UVertexType.get_db_table_name()
    print UEdgeType.get_db_table_name()
    print UVertexType.get_const_attributes()