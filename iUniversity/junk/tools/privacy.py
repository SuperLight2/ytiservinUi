__author__ = 'gumerovif'


class ResourceRestriction(object):
    PUBLIC = 1
    PRIVATE = 2


class GroupPermission(object):
    GUEST = 1
    MEMBER = 2
    ADMIN = 3


class Privacy(object):
    @classmethod
    def allowed_to_read(cls, permission, restriction):
        return \
            (permission in [GroupPermission.ADMIN, GroupPermission.MEMBER]) \
                or (permission == GroupPermission.GUEST and restriction == ResourceRestriction.PUBLIC)

