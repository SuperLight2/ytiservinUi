__author__ = 'gumerovif'

from core.u_vertex_types.vertex_types import UVertexTypes
from core.u_vertex_types.user import UUserType
from core.u_vertex_types.group import UGroupType
from core.u_vertex_types.resource import UResourceType

from core.u_edge_types.edge_types import UEdgeTypes
from core.u_edge_types.member_of_group import UMemberOfGroup
from core.u_edge_types.friends import UFriends
from core.u_edge_types.like import ULike
from core.u_edge_types.liked_by import ULikedBy


class UTypes(object):
    MAPPING = {
        UVertexTypes.USER: UUserType,
        UVertexTypes.GROUP: UGroupType,
        UVertexTypes.RESOURCE: UResourceType,
        UEdgeTypes.MEMBER_OF_GROUP: UMemberOfGroup,
        UEdgeTypes.FRIENDS: UFriends,
        UEdgeTypes.LIKE: ULike,
        UEdgeTypes.LIKED_BY: ULikedBy,
        UEdgeTypes.NONE_EDGE: None,
    }

    @classmethod
    def get(cls, u_type_index):
        return cls.MAPPING[u_type_index]


if __name__ == '__main__':
    print UTypes.get(UVertexTypes.USER)
    print UTypes.get(UEdgeTypes.MEMBER_OF_GROUP)