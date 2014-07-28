__author__ = 'gumerovif'

from core.u_field import UField


class UType(object):
    _db_table_name = UField.Virtual()

    @classmethod
    def _get_all_fields(cls):
        result = dict()
        for pcls in cls.__mro__:
            if pcls is object:
                continue
            for attr_name, attr in pcls.__dict__.iteritems():
                if not isinstance(attr, UField):
                    continue
                result[attr_name] = attr
        return result

    @classmethod
    def get_const_attributes(cls):
        result = dict()
        for attr_name, attr in cls._get_all_fields().iteritems():
            if attr.is_constant():
                result[attr_name] = attr.get_const_value()
        return result

    @classmethod
    def get_db_table_name(cls):
        return cls._db_table_name.get_const_value()

    """@classmethod
    def get_data_template(cls):
        result = {}
        for key, field in cls.get_data_attributes().iteritems():
            value_type = field.get_field_type()
            result[key] = value_type()
        return result"""

    @classmethod
    def validate(cls):
        for attr_name, attr in cls._get_all_fields().iteritems():
            print attr_name, attr
            if attr.is_virtual():
                raise BaseException("Found virtual field: %s" % attr_name)

    @classmethod
    def check_value(cls, **kwargs):
        attrs = cls._get_all_fields()
        for attr_name, attr_value in kwargs.iteritems():
            if attr_name not in attrs:
                raise BaseException("Unknown attribute: %s" % attr_name)
            attrs[attr_name].check_value(attr_value)


class UVertexType(UType):
    _db_table_name = UField.Constant('u_vertices') # HOW TO REWRITE THIS?

    uid = UField.RequiredInteger()
    utype = UField.RequiredShortInteger()
    deleted = UField.RequiredBoolean()


class UEdgeType(UType):
    _db_table_name = UField.Constant('u_edges')

    uid1_type = UField.Virtual()
    uid2_type = UField.Virtual()
    inverse_type = UField.Virtual()

    uid1 = UField.RequiredInteger()
    uid2 = UField.RequiredInteger()
    timestamp = UField.RequiredInteger()
    info = UField.RequiredString()
    deleted = UField.RequiredBoolean()


if __name__ == '__main__':
    UVertexType.check_value(uid=1, utype=2)
    UVertexType().validate()
    try:
        UEdgeType().validate()
    except BaseException, e:
        print e
    print UVertexType.get_db_table_name()
    print UEdgeType.get_db_table_name()
    print UVertexType.get_const_attributes()