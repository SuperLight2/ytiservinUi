__author__ = 'gumerovif'

from core.u_type import UVertexType
from core.u_field import UField


class UUserType(UVertexType):
    lastname = UField.String()
    firstname = UField.String()
    gender = UField.Integer()


if __name__ == '__main__':
    print [(f, v.const_value) for f, v in UUserType.get_const_attributes().iteritems()]
    print UUserType.get_data_attributes()