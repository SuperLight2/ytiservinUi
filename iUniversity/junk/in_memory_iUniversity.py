from tools.groups import GroupsHierarchy, GroupType
from tools.resources import Resource
from tools.users import User
from tools.privacy import ResourceRestriction, GroupPermission


def main():
    groups_hierarchy = GroupsHierarchy()

    # groups hierarchy
    usatu = groups_hierarchy.add_group(GroupType.UNIVERSITY, "USATU")
    am_group = groups_hierarchy.add_group(GroupType.STUDENTS_GROUP, "Applied Mathematics", usatu)
    ami_group = groups_hierarchy.add_group(GroupType.STUDENTS_GROUP, "Applied Mathematics and Inf", usatu)

    msu = groups_hierarchy.add_group(GroupType.UNIVERSITY, "Meleuz Gov University")
    hu_group = groups_hierarchy.add_group(GroupType.STUDENTS_GROUP, "HU group", msu)
    hui_group = groups_hierarchy.add_group(GroupType.STUDENTS_GROUP, "HUI group", msu)

    # resources
    res1 = Resource()
    res2 = Resource()
    res3 = Resource()
    res4 = Resource()

    # users
    usatu_admin = User("Admin", "Usatu").id
    am_member = User("AM", "Member").id
    hui_admin = User("HUI", "Admin").id
    guest = User("Super", "Guest").id

    # adding
    usatu.add_resource(res1, ResourceRestriction.PUBLIC)
    am_group.add_resource(res2, ResourceRestriction.PRIVATE)
    msu.add_resource(res3, ResourceRestriction.PRIVATE)
    hui_group.add_resource(res4, ResourceRestriction.PUBLIC)

    usatu.add_user(usatu_admin, GroupPermission.ADMIN)
    am_group.add_user(am_member, GroupPermission.MEMBER)
    hui_group.add_user(hui_admin, GroupPermission.ADMIN)

    print groups_hierarchy.get_resources_for_user(usatu_admin)
    print groups_hierarchy.get_resources_for_user(am_member)
    print groups_hierarchy.get_resources_for_user(hui_admin)
    print groups_hierarchy.get_resources_for_user(guest)


if __name__ == '__main__':
    main()
