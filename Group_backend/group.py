import logging

from django.db import IntegrityError

from Group_backend.models import Group
from User_backend.user import get_user_details, get_user_object

log = logging.getLogger(__name__)

def get_group_object(user, group_name):
    try:
        return user.group_set.get(name = group_name)
    except Group.DoesNotExist, e:
        log.error('New Group with name = "' + group_name + '" and user = "' + \
                  user.email + '" could not be created - "' + str(e) + '"')
        return None

def create_group(user, group_name, color = ''):
    group = Group(user = user, name = group_name, color = color)
    try:
        group.save()
    except IntegrityError, e:
        log.error('New Group with name = "' + group_name + '" and user = "' + \
                  user.email + '" could not be created - "' + str(e) + '"')

def create_default_groups(user):
    create_group(user = user, name = 'Home', color = '#2EFF00')
    create_group(user = user, name = 'Friends', color = '#E9FF00')
    create_group(user = user, name = 'Work', color = '#2E00FF')

def delete_group(user, group_name):
    group = get_group_object(user, group_name)
    if group != None:
        group.delete()
    
def get_members(user, group_name):
    members = []
    if group_name == '':
        for group in user.group_set.all():
            members.append(get_group_details(group))
    else:
        group = get_group_object(user, group_name)
        if group != None:
            members.append(get_group_details(group))
    return members

def get_group_details(group):
    return {"name": group.name, "color": group.color, \
            "members": [get_user_details(i) for i in group.members.all()]}

def add_member_to_group(user, group_name, member_email):
    group = get_group_object(user, group_name)
    if group != None:
        member = get_user_object(member_email)
        group.members.add(member)

def remove_member_from_group(user, group_name, member_email):
    group = get_group_object(user, group_name)
    if group != None:
        member = get_user_object(member_email)
        group.members.remove(member)
