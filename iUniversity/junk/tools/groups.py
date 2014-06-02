__author__ = 'gumerovif'

from id_generator import IDGenerator
from privacy import Privacy
from Queue import Queue


class GroupType(object):
    ROOT = 1
    UNIVERSITY = 2
    STUDENTS_GROUP = 3


class Group:
    def __init__(self, type, name, parent_id):
        self.id = IDGenerator.generate_unique_id()
        self.type = type
        self.name = name
        self.parents = [parent_id]
        self.children = []
        self.resources = dict()
        self.participants = dict()

    def get_id(self):
        return self.id

    def add_resource(self, resource_id, restriction):
        self.resources[resource_id] = restriction

    def add_user(self, user_id, permission):
        self.participants[user_id] = permission

    def add_child_group(self, group_id):
        self.children.append(group_id)

    def get_parents(self):
        return self.parents

    def get_users(self):
        return self.participants

    def get_resources_for_user(self, user_id):
        resources = set()
        permission = self.participants[user_id]
        for resource, restriction in self.resources.iteritems():
            if Privacy.allowed_to_read(permission, restriction):
                resources.add(resource.get_id())
        return resources


class GroupsHierarchy:
    def __init__(self):
        self.root_group = Group(GroupType.ROOT, 'ROOT', None)
        self.root_group_id = self.root_group.get_id()
        self.groups = dict()
        self.groups[self.root_group.get_id()] = self.root_group

    def add_group(self, type, name, parent_group=None):
        if parent_group is None:
            parent_group = self.root_group
        parent_id = parent_group.get_id()
        group = Group(type, name, parent_id)
        self.groups[group.get_id()] = group
        parent_group = self.find_group_by_id(parent_id)
        parent_group.add_child_group(group.get_id())
        return group

    def find_group_by_id(self, group_id):
        return self.groups[group_id]

    def path_to_root(self, group_id):
        result = set()
        queue = Queue()
        queue.put_nowait(group_id)
        while not queue.empty():
            current_group_id = queue.get_nowait()
            if current_group_id == self.root_group_id:
                continue
            group = self.find_group_by_id(current_group_id)
            for parent_id in group.get_parents():
                if parent_id not in result:
                    result.add(parent_id)
                    queue.put_nowait(parent_id)
        return result

    def get_resources_for_user(self, user_id):
        found_group_ids = set()
        for group_id, group in self.groups.iteritems():
            if user_id in group.get_users():
                path_to_root = self.path_to_root(group_id)
                found_group_ids.update(path_to_root)
        resources = set()
        for group_id in found_group_ids:
            group = self.find_group_by_id(group_id)
            resources.update(group.get_resources_for_user(user_id))