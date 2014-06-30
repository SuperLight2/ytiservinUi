__author__ = 'gumerovif'


class UField(object):
    CONST = "const"
    DATA = "data"
    REQUIRED = "required"

    INTEGER = int
    STRING = str
    FLOAT = float
    BOOLEAN = bool

    ALLOWED_TYPES = [INTEGER, STRING, FLOAT, BOOLEAN]
    ALLOWED_PREFIXES = [REQUIRED, CONST, DATA]

    def __init__(self, field_type=None, prefix=DATA, const_value=None):
        self.const_value = const_value
        if self.const_value is None:
            if field_type not in self.ALLOWED_TYPES:
                raise BaseException("Field {0} has not allowed type".format(field_type))
            if prefix not in self.ALLOWED_PREFIXES:
                raise BaseException("Prefix {0} is not allowed".format(prefix))
        else:
            prefix = self.CONST
        self.field_type = field_type
        self.prefix = prefix

    @classmethod
    def RequiredInteger(cls):
        return UField(field_type=UField.INTEGER, prefix=UField.REQUIRED)

    @classmethod
    def RequiredString(cls):
        return UField(field_type=UField.STRING, prefix=UField.REQUIRED)

    @classmethod
    def Constant(cls, const_value):
        return UField(const_value=const_value)

    @classmethod
    def Integer(cls):
        return UField(field_type=UField.INTEGER, prefix=UField.DATA)

    @classmethod
    def String(cls):
        return UField(field_type=UField.STRING, prefix=UField.DATA)

    def get_field_type(self):
        return self.field_type
