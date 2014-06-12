__author__ = 'gumerovif'

from core.u_type import UVertexType
from core.u_field import UField


class UUserType(UVertexType):
    lastname = UField(field_type=str)
    firstname = UField(field_type=str)
    gender = UField(field_type=int)


if __name__ == '__main__':
    print UUserType.get_attributes()
    print [(f, v.const_value) for f, v in UUserType.get_attributes("const").iteritems()]
    print UUserType.get_attributes("data")