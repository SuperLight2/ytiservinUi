__author__ = 'gumerovif'


class UField(object):
    CONST_FIELD = "const"
    DATA_FIELD = "data"
    VIRTUAL_FIELD = "virtual"

    SHORT_INTEGER = (int, 'int(11) NOT NULL DEFAULT 0')
    INTEGER = (int, 'bigint(20) NOT NULL DEFAULT 0')
    STRING = (str, 'varchar(255) NOT NULL DEFAULT \'\'')
    TEXT = (str, 'text NOT NULL DEFAULT \'\'')
    BOOLEAN = (bool, 'boolean NOT NULL DEFAULT 0')

    def __init__(self, field_class=DATA_FIELD, field_type=None, const_value=None, nullable=True):
        self._field_class = field_class
        if field_class == UField.VIRTUAL_FIELD:
            pass
        elif field_class == UField.CONST_FIELD:
            self._const_value = const_value
        elif field_class == UField.DATA_FIELD:
            self._field_type, self._sql_field_type = field_type
            self.nullable = nullable
        else:
            raise BaseException("Unknown class {0}".format(field_class))

    @classmethod
    def RequiredInteger(cls):
        return UField(field_type=UField.INTEGER, field_class=UField.DATA_FIELD, nullable=False)

    @classmethod
    def RequiredShortInteger(cls):
        return UField(field_type=UField.SHORT_INTEGER, field_class=UField.DATA_FIELD, nullable=False)

    @classmethod
    def RequiredString(cls):
        return UField(field_type=UField.STRING, field_class=UField.DATA_FIELD, nullable=False)

    @classmethod
    def RequiredBoolean(cls):
        return UField(field_type=UField.BOOLEAN, field_class=UField.DATA_FIELD, nullable=False)

    @classmethod
    def Constant(cls, const_value):
        return UField(field_class=UField.CONST_FIELD, const_value=const_value)

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

    def is_virtual(self):
        return self._field_class == UField.VIRTUAL_FIELD

    def is_nullable(self):
        return self.nullable

    def is_constant(self):
        return self._field_class == UField.CONST_FIELD

    def is_data_field(self):
        return self._field_class == UField.DATA_FIELD

    def check_value(self, value):
        if self.is_virtual():
            raise BaseException("This field is virtual, can't set the value")
        if self.is_constant():
            raise BaseException("This field is constant, can't edit the value")
        if (not self.is_nullable()) and (value is None):
            raise BaseException("This value can't be null")
        if not isinstance(value, self._field_type):
            raise BaseException("Wrong type, expected " + str(self._field_type) + ", got " + str(type(value)))

    def get_const_value(self):
        if not self.is_constant():
            raise BaseException("This field is not constant!")
        return self._const_value


if __name__ == '__main__':
    # TESTS TESTS TESTS
    f = UField.Constant("tests")
    try:
        f.check_value(None)
    except BaseException, e:
        print e
    print f.get_const_value()

    f = UField.RequiredInteger()
    try:
        f.check_value(None)
    except BaseException, e:
        print e
    f.check_value(5)

    try:
        f.check_value("1223")
    except BaseException, e:
        print e

    f = UField.Virtual()
    try:
        f.check_value(None)
    except BaseException, e:
        print e