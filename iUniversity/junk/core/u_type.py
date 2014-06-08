__author__ = 'gumerovif'


class UType(object):
    ALLOWED_TYPES = [int, str, float, tuple, dict]
    REQUIRED_PREFIX = 'required'
    CONST_PREFIX = 'const'

    required_uid = int
    required_utype = str

    @classmethod
    def _get_attributes(cls):
        for pcls in cls.__mro__:
            if pcls is object:
                continue
            for attr_name, attr in pcls.__dict__.iteritems():
                yield attr_name, attr

    @classmethod
    def get_key_values(cls):
        result = []
        for attr_name, attr in cls._get_attributes():
            if attr_name.startswith(UType.REQUIRED_PREFIX):
                result.append((attr_name, attr))
        return result

    @classmethod
    def get_constants(cls):
        for attr_name, attr in cls._get_attributes():
            if attr_name.startswith(UType.CONST_PREFIX):
                yield attr_name, attr

    @classmethod
    def validate(cls):
        for attr_name, attr in cls.get_key_values():
            if attr not in UType.ALLOWED_TYPES:
                raise BaseException("Key {0} has not allowed value type".format(attr_name))
        for attr_name, attr in cls.get_constants():
            if attr is None:
                raise BaseException("Key {0} has None value".format(attr_name))


class UVertexType(UType):
    pass


class UEdgeType(UType):
    const_uid1_type = None
    const_uid2_type = None
    const_direction = None
    const_inverse_type = None

    required_uid1 = int
    required_uid2 = int
    required_timestamp = int
    required_info = str


def validate_u_type():
    # go through the all subclasses of UType and call validate() function
    pass


if __name__ == '__main__':
    UType.validate()
    UVertexType.validate()
    UEdgeType.validate()