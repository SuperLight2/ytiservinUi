__author__ = 'gumerovif'


class UField(object):
    CONST_FIELD = "const"
    DATA_FIELD = "data"
    REQUIRED_FIELD = "required"
    VIRTUAL_FIELD = "virtual"

    SHORT_INTEGER = (int, 'int(11) NOT NULL DEFAULT 0')
    INTEGER = (int, 'bigint(20) NOT NULL DEFAULT 0')
    STRING = (str, 'varchar(255) NOT NULL DEFAULT \'\'')
    TEXT = (str, 'text NOT NULL DEFAULT \'\'')
    BOOLEAN = (bool, 'boolean NOT NULL DEFAULT 0')

    def __init__(self, field_class=DATA_FIELD, field_type=None, const_value=None):
        self.field_class = field_class
        if field_class == UField.VIRTUAL_FIELD:
            return
        if field_class == UField.CONST_FIELD:
            self.const_value = const_value
        if (field_class == UField.DATA_FIELD) or (field_class == UField.REQUIRED_FIELD):
            self.field_type, self.sql_field_type = field_type
        raise BaseException("Class {0} is not allowed".format(field_class))

    @classmethod
    def RequiredInteger(cls):
        return UField(field_type=UField.INTEGER, field_class=UField.REQUIRED_FIELD)

    @classmethod
    def RequiredShortInteger(cls):
        return UField(field_type=UField.SHORT_INTEGER, field_class=UField.REQUIRED_FIELD)

    @classmethod
    def RequiredString(cls):
        return UField(field_type=UField.STRING, field_class=UField.REQUIRED_FIELD)

    @classmethod
    def RequiredBoolean(cls):
        return UField(field_type=UField.BOOLEAN, field_class=UField.REQUIRED_FIELD)

    @classmethod
    def Constant(cls, const_value):
        return UField(const_value=const_value)

    @classmethod
    def Virtual(cls):
        return UField(field_class=UField.VIRTUAL_FIELD)

    @classmethod
    def Integer(cls):
        return UField(field_type=UField.INTEGER, field_class=UField.DATA_FIELD)

    @classmethod
    def ShortInteger(cls):
        return UField(field_type=UField.SHORT_INTEGER, field_class=UField.DATA_FIELD)

    @classmethod
    def String(cls):
        return UField(field_type=UField.STRING, field_class=UField.DATA_FIELD)

    @classmethod
    def Text(cls):
        return UField(field_type=UField.TEXT, field_class=UField.DATA_FIELD)

    def get_field_type(self):
        return self.field_type

    def get_sql_field_type(self):
        return self.sql_field_type

    def get_field_class(self):
        return self.field_class

    def is_virtual(self):
        return self.field_class == UField.VIRTUAL_FIELD
