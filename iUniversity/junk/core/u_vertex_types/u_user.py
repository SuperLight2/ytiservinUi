__author__ = 'gumerovif'

from core.u_type import UVertexType


class UUserType(UVertexType):
    required_last_name = str
    required_first_name = str
    required_gender = int
