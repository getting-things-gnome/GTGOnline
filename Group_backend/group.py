import logging

from django.db import IntegrityError

from Group_backend.models import Group
from User_backend.user import get_user_details

log = logging.getLogger(__name__)

def create_group(user, group_name, color = ''):
    group = Group(user = user, name = group_name, color = color)
    try:
        group.save()
    except IntegrityError, e:
        log.error('New Group with name = "' + group_name + '" and user = "' + \
                  user.email + '" could not be created - "' + str(e) + '"')
    
def get_group_object(user, group_name):
    try:
        return Group.objects.get(user = user.pk, name = group_name)
    except Group.DoesNotExist:
        return None
    
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
