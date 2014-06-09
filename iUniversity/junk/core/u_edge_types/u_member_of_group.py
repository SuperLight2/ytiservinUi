__author__ = 'gumerovif'

from core.u_type import UEdgeType
from core.u_field import UField
from core.u_vertex_types.u_vertex_types import UVertexTypes


class UMemberOfGroup(UEdgeType):
    uid1_type = UField(const_value=UVertexTypes.USER)
    uid2_type = UField(const_value=UVertexTypes.GROUP)
    direction = UField(const_value="BIDIRECTIONAL")


if __name__ == '__main__':
    print UMemberOfGroup.get_attributes()
    print [(f, v.const_value) for f, v in UMemberOfGroup.get_attributes("const").iteritems()]
    print UMemberOfGroup.get_attributes("data")