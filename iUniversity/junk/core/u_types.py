__author__ = 'gumerovif'

from core.u_vertex_types.u_vertex_types import UVertexTypes
from core.u_vertex_types.u_user import UUserType
from core.u_vertex_types.u_group import UGroupType
from core.u_vertex_types.u_resource import UResourceType

from core.u_edge_types.u_edge_types import UEdgeTypes
from core.u_edge_types.u_member_of_group import UMemberOfGroup


class UTypes(object):
    MAPPING = {
        UVertexTypes.USER: UUserType,
        UVertexTypes.GROUP: UGroupType,
        UVertexTypes.RESOURCE: UResourceType,
        UEdgeTypes.MEMBER_OF_GROUP: UMemberOfGroup
    }

    @classmethod
    def get(cls, u_type_index):
        return cls.MAPPING.get(u_type_index, None)


if __name__ == '__main__':
    print UTypes.get(UVertexTypes.USER)
    print UTypes.get(UEdgeTypes.MEMBER_OF_GROUP)