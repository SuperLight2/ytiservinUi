__author__ = 'gumerovif'

from core.u_type import UEdgeType
from core.u_field import UField
from core.u_vertex_types.vertex_types import UVertexTypes


class UMemberOfGroup(UEdgeType):
    uid1_type = UField.Constant(UVertexTypes.USER)
    uid2_type = UField.Constant(UVertexTypes.GROUP)
    inverse_type = UField.Constant(None)


if __name__ == '__main__':
    print [(f, v, v.const_value) for f, v in UMemberOfGroup.get_const_attributes().iteritems()]
    UMemberOfGroup.validate()