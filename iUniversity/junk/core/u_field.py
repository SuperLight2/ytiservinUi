__author__ = 'gumerovif'


class UField(object):
    CONST = "const"
    DATA = "data"

    ALLOWED_TYPES = [int, str, float, tuple, dict]
    ALLOWED_PREFIXES = ["", "const", "data"]

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

    def get_field_type(self):
        return self.field_type

