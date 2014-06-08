__author__ = 'gumerovif'

from core.u_vertex_types.u_user import UUserType
from core.u_vertex_types.u_group import UGroupType
from core.u_vertex_types.u_resource import UResourceType

from core.u_edge_types.u_member_of_group import UMemberOfGroup


# make these classes automatically generated
class UTypes(object):
    MAPPING = dict()

    @classmethod
    def get(cls, u_type_index):
        return cls.MAPPING.get(u_type_index, None)


class UVertexTypes(UTypes):
    USER = 1
    GROUP = 2
    RESOURCE = 3

    MAPPING = {
        USER: UUserType,
        GROUP: UGroupType,
        RESOURCE: UResourceType,
    }


class UEdgeTypes(UTypes):
    MEMBER_OF_GROUP = 4

    MAPPING = {
        MEMBER_OF_GROUP: UMemberOfGroup
    }


if __name__ == '__main__':
    print UVertexTypes.get(UVertexTypes.USER)
    print UVertexTypes.get(UEdgeTypes.MEMBER_OF_GROUP)