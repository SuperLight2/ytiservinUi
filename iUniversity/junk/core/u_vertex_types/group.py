__author__ = 'gumerovif'

from core.u_type import UVertexType
from core.u_field import UField


class UGroupType(UVertexType):
    name = UField.String()
    description = UField.String()
