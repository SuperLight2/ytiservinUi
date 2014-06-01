from time import time

class ResourceRestriction(object):
    PUBLIC = 1
    PRIVATE = 2


class GroupPermission(object):
    GUEST = 1
    MEMBER = 2
    ADMIN = 3


class GroupType(object):
    ROOT = 1
    UNIVERSITY = 2
    STUDENTS_GROUP = 3


class Resource:
    def __init__(self):
        self.id = IDGenerator.generate_unique_id()
        self.mod_timestamps = [time()]


class Group:
    def __init__(self, type, name, parent_id):
        self.id = IDGenerator.generate_unique_id()
        self.type = type
        self.name = name
        self.parents = [parent_id]
        self.resources = dict()
        self.participants = dict()

    #map<int, ResourceRestriction> resources,
    #map<int, GroupPermission> participants,


class User:
    def __init__(self, first_name, last_name):
        self.id = IDGenerator.generate_unique_id()
        self.first_name = first_name
        self.last_name = last_name

    #set<int64> inGroups,


def main():
    pass


if __name__ == '__main__':
    main()
