__author__ = 'gumerovif'

from core.u_type import UEdgeType
from core.u_field import UField
from core.u_vertex_types.vertex_types import UVertexTypes
from core.u_edge_types.edge_types import UEdgeTypes


class ULikedBy(UEdgeType):
    UEdgeType.uid1_type = UField.Constant(UVertexTypes.RESOURCE)
    UEdgeType.uid2_type = UField.Constant(UVertexTypes.USER)
    UEdgeType.inverse_type = UField.Constant(UEdgeTypes.LIKE)
