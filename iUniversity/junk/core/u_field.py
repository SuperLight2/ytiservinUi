__author__ = 'gumerovif'


class UField(object):
    CONST_FIELD = "const"
    DATA_FIELD = "data"
    REQUIRED_FIELD = "required"
    VIRTUAL_FIELD = "virtual"

    INTEGER = int
    STRING = str
    FLOAT = float
    BOOLEAN = bool

    ALLOWED_TYPES = [INTEGER, STRING, FLOAT, BOOLEAN]
    ALLOWED_CLASSES = [REQUIRED_FIELD, CONST_FIELD, DATA_FIELD, VIRTUAL_FIELD]

    def __init__(self, field_type=None, field_class=DATA_FIELD, const_value=None):
        self.const_value = const_value
        if self.const_value is None:
            if field_type not in self.ALLOWED_TYPES:
                raise BaseException("Field {0} has not allowed type".format(field_type))
            if field_class not in self.ALLOWED_CLASSES:
                raise BaseException("Class {0} is not allowed".format(field_class))
        else:
            field_class = self.CONST_FIELD
        self.field_type = field_type
        self.field_class = field_class

    @classmethod
    def RequiredInteger(cls):
        return UField(field_type=UField.INTEGER, field_class=UField.REQUIRED_FIELD)

    @classmethod
    def RequiredString(cls):
        return UField(field_type=UField.STRING, field_class=UField.REQUIRED_FIELD)

    @classmethod
    def Constant(cls, const_value):
        return UField(const_value=const_value)

    @classmethod
    def Virtual(cls):
        return UField(field_class=UField.VIRTUAL_FIELD, field_type=UField.INTEGER)

    @classmethod
    def Integer(cls):
        return UField(field_type=UField.INTEGER, field_class=UField.DATA_FIELD)

    @classmethod
    def String(cls):
        return UField(field_type=UField.STRING, field_class=UField.DATA_FIELD)

    def get_field_type(self):
        return self.field_type

    def get_field_class(self):
        return self.field_class

    def is_virtual(self):
        return self.field_class == UField.VIRTUAL_FIELD
