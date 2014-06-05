__author__ = 'gumerovif'

from core.u_type import UEdgeType


class UMemberOfGroup(UEdgeType):
    const_uid1_type = 'USER'
    const_uid2_type = 'GROUP'
    const_direction = 'BIDIRECTIONAL'
    const_inverse_type = '???'
