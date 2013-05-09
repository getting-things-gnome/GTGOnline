import re

from Tag_backend.models import Tag
from Task_backend.task import get_task_object
from User_backend.user import get_user_object
from GTGOnline.static import *

def find_tags(text):
    return re.findall(TAG_REGEX, text)

def does_tag_exist(user, tag_name):
    return Tag.objects.filter(user = user, name = tag_name).exists()

def create_tag_objects(user, task_id, text):
    user = get_user_object(user)
    tag_objects = []
    tag_list = find_tags(text)
    for tag in tag_list:
        tag = tag[1:]
        if does_tag_exist(user, tag):
            update_task_set(user, task_id, tag)
        else:
            new_tag = Tag(user = user, name = tag)
            update_task_set(user, task_id, tag)
            tag_objects.append(new_tag)
    return tag_objects

def create_bulk_tags(user, task_id, text):
    tag_objects = create_tag_objects(user, task_id, text)
    Tag.objects.bulk_create(tag_objects)
    
def get_tag_object(user, tag_name = None, tag_id = None):
    user = get_user_object(user)
    if tag_id != None:
        return Tag.objects.get(user = user, id = tag_id)
    if tag_name != None:
        return Tag.objects.get(user = user, name = tag_name)

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
def update_task_set(user, task_id, tag_name):
    task = get_task_object(user, task_id)
    tag = get_tag_object(user, tag_name = tag_name)
    tag.task_set.add(task)
    
def delete_tag(user, tag_name = None, tag_id = None):
    tag = get_tag_object(user, tag_name, tag_id)
    tag.delete()
        
def get_task_count(user, tag_name = None, tag_id = None):
    tag = get_tag_object(user, tag_name, tag_id)
    return tag.task_set.count()




    





    

