import re
import json

from Tag_backend.models import Tag
from User_backend.user import get_user_object
from Tools.constants import *

def find_tags(text):
    tags_list = re.findall(TAG_REGEX, text)
    tags_list = [x[1:].lower() for x in tags_list]
    return list(set(tags_list))

def does_tag_exist(user, tag_name):
    return user.tag_set.filter(name = tag_name).exists()

def create_tag_objects(user, tag_list):
    '''
    It takes a user object and a tag_list containing tag names obtained from
    find_tags(), and returns a tuple of
    (list of new tags created and saved, list of existing tags)
    '''
    user = get_user_object(user)
    new_tags, existing_tags, new_tags_names = [], [], []
    for tag in tag_list:
        if does_tag_exist(user, tag):
            existing_tags.append(get_tag_object(user, tag_name = tag))
        else:
            created_tag = Tag(user = user, name = tag)
            new_tags.append(created_tag)
            new_tags_names.append(tag)
    
    if new_tags != []:
        create_bulk_tags(new_tags)
        # bulk_create does not return the ids of the objects saved. Hence, we
        # cannot use the new_tags list as it has not been updated. So, we have
        # to run another query which gets those same objects again from the
        # database.
        new_tags = Tag.objects.filter(user = user, name__in = new_tags_names)
        # For existing tags, we can simply give their list to the task object,
        # and it will add it to it's m2m field. Note that the following approach
        # only works because the existing tags HAVE ids.
        #task_object.tags.add(*existing_tags)
    return (list(new_tags), existing_tags)

def create_bulk_tags(tag_objects):
    Tag.objects.bulk_create(tag_objects)
    
def get_tags_details(task):
    tags = []
    for tag in task.tags.all():
        tags.append({"name": tag.name, "color": tag.color, "icon": tag.icon})
    return tags

def get_tag_object(user, tag_name = None, tag_id = None):
    #user = get_user_object(user)
    if tag_id != None:
        try:
            return Tag.objects.get(user = user, id = tag_id)
        except Tag.DoesNotExist:
            return None
    if tag_name != None:
        try:
            return Tag.objects.get(user = user, name = tag_name)
        except Tag.DoesNotExist:
            return None

def update_tag_name(user, tag_id, new_name):
    user = get_user_object(user)
    tag = Tag.objects.get(user = user, id = tag_id)
    tag.name = new_name
    tag.save()
    
def update_tag_color(user, tag_id, new_color):
    user = get_user_object(user)
    tag = Tag.objects.get(user = user, id = tag_id)
    tag.color = new_color
    tag.save()
    
def update_tag_icon(user, tag_id, new_icon):
    user = get_user_object(user)
    tag = Tag.objects.get(user = user, id = tag_id)
    tag.icon = new_icon
    tag.save()
    
# Instead of using this function, use Task.tags.add(tag) in task.py
def update_task_set(user, task, tag):
    tag.task_set.add(task)
    
def delete_tag(user, tag_name = None, tag_id = None):
    tag = get_tag_object(user, tag_name, tag_id)
    tag.delete()
        
def get_task_count(user, tag_name = None, tag_id = None):
    tag = get_tag_object(user, tag_name, tag_id)
    return tag.task_set.count()
