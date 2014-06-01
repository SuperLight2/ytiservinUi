from IDGenerator.IDGenerator import IDGenerator
from datetime import datetime


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
        self.mod_timestamps = [datetime.now()]


class Group:
    def __init__(self, type, name, parent_id):
        self.id = IDGenerator.generate_unique_id()
        self.type = type
        self.name = name
        self.parents = [parent_id]
        self.resources = dict()
        self.participants = dict()

    def add_resource(self, resource_id, restriction):
        self.resources[resource_id] = restriction

    def add_user(self, user_id, permission):
        self.participants[user_id] = permission

class GroupsHierarchy:
    def __init__(self):
        root_group = Group(GroupType.ROOT, 'ROOT', None)
        self.groups = [root_group]

    def add_group(self, type, name, parent_id):
        group = Group(type, name, parent_id)
        self.groups[] = group

    def find_group_by_id(self, group_id):
        raise BaseException("Not Implemented")

    def get_resources_for_user(self):
        raise BaseException("Not Implemented")


class User:
    def __init__(self, first_name, last_name):
        self.id = IDGenerator.generate_unique_id()
        self.first_name = first_name
        self.last_name = last_name
        self.in_groups = set()


def main():
    pass


if __name__ == '__main__':
    main()
