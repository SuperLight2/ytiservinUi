__author__ = 'gumerovif'

from core.u_field import UField


class UType(object):
    _db_table_name = None

    @classmethod
    def _get_all_attributes(cls):
        for pcls in cls.__mro__:
            if pcls is object:
                continue
            for attr_name, attr in pcls.__dict__.iteritems():
                yield attr_name, attr

    @classmethod
    def _get_attributes(cls, field_class):
        result = {}
        for attr_name, attr in cls._get_all_attributes():
            if not isinstance(attr, UField):
                continue
            if attr.get_field_class() == field_class:
                result[attr_name] = attr
        return result

    @classmethod
    def get_const_attributes(cls):
        return cls._get_attributes(UField.CONST_FIELD)

    @classmethod
    def get_data_attributes(cls):
        return cls._get_attributes(UField.DATA_FIELD)

    @classmethod
    def get_db_table_name(cls):
        return cls._db_table_name

    @classmethod
    def get_table_creation_sql(cls):
        cls.validate()
        result = "CREATE TABLE %s (\n" % cls.get_db_table_name()
        for name, field in cls._get_attributes(UField.REQUIRED_FIELD).iteritems():
            result += "  %s %s,\n" % (name, field.get_sql_field_type())
        result += ")"
        raise BaseException("Wrong implementation")

    @classmethod
    def validate(cls):
        for name, attr in cls._get_attributes(UField.VIRTUAL_FIELD).iteritems():
            if attr.is_virtual():
                raise BaseException("Virtual field are not allowed: %s" % name)

    @classmethod
    def get_data_template(cls):
        result = {}
        for key, field in cls.get_data_attributes().iteritems():
            value_type = field.get_field_type()
            result[key] = value_type()
        return result


class UVertexType(UType):
    _db_table_name = 'u_vertices'

    uid = UField.RequiredInteger()
    utype = UField.RequiredShortInteger()
    deleted = UField.RequiredBoolean()


class UEdgeType(UType):
    _db_table_name = 'u_edges'

    uid1_type = UField.Virtual()
    uid2_type = UField.Virtual()
    inverse_type = UField.Virtual()

    uid1 = UField.RequiredInteger()
    uid2 = UField.RequiredInteger()
    timestamp = UField.RequiredInteger()
    info = UField.RequiredString()
    deleted = UField.RequiredBoolean()


if __name__ == '__main__':
    UVertexType.validate()
    #UEdgeType.validate() # must raise an exception!
    print UVertexType.get_db_table_name()
    print UEdgeType.get_db_table_name()
