import logging

from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import get_user_model

from Group_backend.models import Group
from User_backend.user import get_user_details, get_user_object
from Tools.constants import *

User = get_user_model()
log = logging.getLogger(__name__)

def get_group_object(user, group_name):
    try:
        return user.group_set.get(name = group_name)
    except Group.DoesNotExist, e:
        log.error('Group with name = "' + group_name + '" and user = "' + \
                  user.email + '" does not exist - "' + str(e) + '"')
        return None

def create_group(user, group_name, color = ''):
    group = Group(user = user, name = group_name, color = color)
    try:
        group.save()
    except IntegrityError, e:
        log.error('New Group with name = "' + group_name + '" and user = "' + \
                  user.email + '" could not be created - "' + str(e) + '"')

def create_default_groups(user):
    create_group(user, 'Home', color = '#2EFF00')
    create_group(user, 'Friends', color = '#E9FF00')
    create_group(user, 'Work', color = '#2E00FF')

def delete_group(user, group_name):
    group = get_group_object(user, group_name)
    if group != None:
        group.delete()
    
def get_members(user, group_name, visited = []):
    members = []
    if group_name == '':
        for group in user.group_set.all():
            members.append(get_group_details(group, group.members.all()))
    elif group_name.lower() == 'others':
        members.append(get_group_details(None, User.objects.all(), \
                                         visited = visited))
    else:
        group = get_group_object(user, group_name)
        if group != None:
            members.append(get_group_details(group, group.members.all()))
    return members

def get_group_details(group, query_set, visited = []):
    members = []
    if group == None:
        for i in query_set:
            if i.email not in visited:
                members.append(get_user_details(i))
        return {"name": "Others", "color": "#F2F2F2", \
            "members": members}
    return {"name": group.name, "color": group.color, \
            "members": [get_user_details(i) for i in query_set]}

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

def find_users_from_query(user, query, origin, visited = []):
    result = []
    if origin == NON_GROUPED:
        users = User.objects.filter(Q(email__icontains = query) | \
                                    Q(first_name__icontains = query) | \
                                    Q(last_name__icontains = query))
        result.append(get_group_details(None, users, visited = visited))
    else:
        for group in user.group_set.all():
            users = group.members.filter(Q(email__icontains = query) | \
                                         Q(first_name__icontains = query) | \
                                         Q(last_name__icontains = query))
            result.append(get_group_details(group, users))
    
    return result
