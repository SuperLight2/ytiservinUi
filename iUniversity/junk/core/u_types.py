__author__ = 'gumerovif'

from core.u_vertex_types.u_user import UUserType
from core.u_vertex_types.u_group import UGroupType
from core.u_vertex_types.u_resource import UResourceType

from core.u_edge_types.u_member_of_group import UMemberOfGroup

# make these classes automatically generated
class UVertexTypes(object):
    USER = UUserType
    GROUP = UGroupType
    RESOURCE = UResourceType


class UEdgeTypes(object):
    MEMBER_OF_GROUP = UMemberOfGroup


if __name__ == '__main__':
    print UEdgeTypes["MEMBER_OF_GROUP"]