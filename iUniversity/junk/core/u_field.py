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
        self._value = None
        self._initialized = False
        self._field_class = field_class
        self.nullable = nullable
        if field_class == UField.VIRTUAL_FIELD:
            pass
        elif field_class == UField.CONST_FIELD:
            self._value, self._initialized = const_value, True
        elif field_class == UField.DATA_FIELD:
            self._field_type, self._sql_field_type = field_type
            if nullable:
                self._value, self._initialized = None, True
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

    def is_initialized(self):
        return self._initialized

    def set_value(self, value):
        if self.is_virtual():
            raise BaseException("This field is virtual, can't set the value")
        if self.is_constant():
            raise BaseException("This field is constant, can't edit the value")
        if (self.is_nullable()) and (value is None):
            self._initialized, self._value = True, value
            return
        if not isinstance(value, self._field_type):
            raise BaseException("Wrong type, expected " + str(self._field_type) + ", got " + str(type(value)))
        self._initialized, self._value = True, value

    def get_value(self):
        if self.is_virtual():
            raise BaseException("This field is virtual, can't return the value")
        if not self.is_initialized():
            raise BaseException("The value is not inited")
        return self._value


if __name__ == '__main__':
    # TESTS TESTS TESTS
    f = UField.Constant(3)
    print f.get_value()
    try:
        f.set_value(5)
    except BaseException, e:
        print e

    f = UField.RequiredInteger()
    try:
        print f.get_value()
    except BaseException, e:
        print e
    f.set_value(5)
    print f.get_value()

    f = UField.Integer()
    try:
        print f.get_value()
    except BaseException, e:
        print e
    try:
        f.set_value("1223")
        print f.get_value()
    except BaseException, e:
        print e
    f.set_value(None)
    print f.get_value()
    f.set_value(111)
    print f.get_value()



