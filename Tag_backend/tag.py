import re
import json
import sys

from Tag_backend.models import Tag
from User_backend.user import get_user_object
from Tools.constants import *
from Tools.dates import get_datetime_str

def find_tags(text):
    #print >>sys.stderr, text + str(type(text))
    tags_list = re.findall(TAG_REGEX, text, re.UNICODE)
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
    
def get_tag_details(tag):
    return {"id": tag.id, "name": tag.name, \
            "color": tag.color, "icon": tag.icon, \
            "count": tag.task_set.count()}

def get_tags_by_task(task):
    tags = []
    for tag in task.tags.all():
        tags.append(get_tag_details(tag))
    return tags

def get_tags_by_user(user):
    tags = []
    for tag in Tag.objects.filter(user = user):
        tags.append(get_tag_details(tag))
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
    tag = get_tag_object(user, tag_id = tag_id)
    if tag == None:
        return
    tag.name = new_name
    tag.save()
    
def update_tag_color(user, tag_id, new_color):
    tag = get_tag_object(user, tag_id = tag_id)
    if tag == None:
        return
    tag.color = new_color
    tag.save()
    
def update_tag_icon(user, tag_id, new_icon):
    tag = get_tag_object(user, tag_id = tag_id)
    if tag == None:
        return
    tag.icon = new_icon
    tag.save()
    
# Instead of using this function, use Task.tags.add(tag) in task.py
def update_task_set(user, task, tag):
    tag.task_set.add(task)

def get_task_count(user, tag_name = None, tag_id = None):
    tag = get_tag_object(user, tag_name, tag_id)
    return tag.task_set.count()

def delete_tag_modify_tasks(user, tag_id):
    tag = get_tag_object(user, tag_id = tag_id)
    if tag == None:
        return
    tag_name = tag.name
    tasks_of_tag = tag.task_set.all()
    for task in tasks_of_tag:
        task.name = task.name.replace('@', '')
        task.description = task.description.replace('@', '')
        task.tags.remove(tag)
        task.save()
    tag.delete()
    return

def delete_orphan_tags(task, tags_list):
    for index, tag in enumerate(tags_list):
        #print >>sys.stderr, "for tag = " + tag.name + " task_set = " + str(tag.task_set.all())
        all_tasks = tag.task_set.all()
        if all_tasks.count() == 0 or ( all_tasks.count() == 1 and task in all_tasks ):
            tag.delete()
