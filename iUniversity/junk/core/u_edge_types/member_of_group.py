__author__ = 'gumerovif'

from core.u_type import UEdgeType
from core.u_field import UField
from core.u_vertex_types.vertex_types import UVertexTypes
from core.u_edge_types.edge_types import UEdgeTypes


class UMemberOfGroup(UEdgeType):
    uid1_type = UField(const_value=UVertexTypes.USER)
    uid2_type = UField(const_value=UVertexTypes.GROUP)
    inverse_type = UField(const_value=UEdgeTypes.NONE_EDGE)


if __name__ == '__main__':
    print UMemberOfGroup.get_attributes()
    print [(f, v.const_value) for f, v in UMemberOfGroup.get_attributes("const").iteritems()]
    print UMemberOfGroup.get_attributes("data")