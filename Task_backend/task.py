import json
import sys

from Task_backend.models import Task
from User_backend.user import get_user_object
from Tag_backend.tag import find_tags, create_tag_objects, get_tags_by_task
from Tools.constants import *
from Tools.dates import get_datetime_object, get_datetime_str, \
                        get_current_datetime_object


def get_task_object(user, task_id):
    try:
        return Task.objects.get(user = user, id = task_id)
    except Task.DoesNotExist:
        return None
    
def get_tasks(username):
    user = get_user_object(username)
    if user != None:
        return Task.objects.filter(user = user)
    else:
        return []

def add_task(user, name, description = "", start_date = None, \
             due_date = None, tag_list = None, parent_id = None):
    user = get_user_object(user)
    start_date = get_datetime_object(user, start_date)
    due_date = get_datetime_object(user, due_date)
    
    new_task = Task(user = user, name = name, description = description, \
                    start_date = start_date, due_date = due_date)
    
    # Try to remove this function and use tag_list obtained from client instead
    tag_list = find_tags(name + " " + description)
    
    new_tags, existing_tags = create_tag_objects(user, tag_list)
    new_task.save()
    new_task.tags.add(*(new_tags+existing_tags))
    
    if parent_id != None:
        parent = get_task_object(user, parent_id)
        new_task.task_set.add(parent)
    
    return new_task

def get_task_details(user, task, indent, visited_list):
    '''
    Takes input an user object and a task object, and returns a dictionary of all
    the task details. This dictionary can then be appended to the JSON object.
    User object is needed to get the datetime in string format based on his
    preferences
    '''
    
    start_date = get_datetime_str(user, task.start_date)
    due_date = get_datetime_str(user, task.due_date)
    closed_date = get_datetime_str(user, task.closed_date)
    last_modified_date = get_datetime_str(user, task.last_modified_date)
    return {"id": task.id, "name": task.name, \
            "description": task.description, \
            "start_date": start_date, "due_date": due_date, \
            "closed_date": closed_date, \
            "last_modified_date": last_modified_date, \
            "status": task.status, "tags": get_tags_by_task(task), \
            "subtasks": get_task_tree(user, \
                                      task.subtasks.filter(status=task.status),\
                                      indent+1, visited_list), \
            "indent": indent}

def get_task_tree(user, task_list, indent, visited_list):
    task_tree = []
    # Initializing visited_list faces problems
    #visited_list = []
    for task in task_list:
        # The following condition will have to changed in the future
        # to enable tasks with multiple parents
        if not visited(task, visited_list):
            task_tree.append(get_task_details(user, task, indent, visited_list))
            visited_list = set_visited(task, visited_list)
            print >>sys.stderr, visited_list
    return task_tree

def update_task_name(user, new_name, task_object, tag_list = None):
    task_object.name = new_name
    
    # Try to remove this function and use tag_list obtained from client instead
    tag_list = find_tags(new_name + " " + task_object.description)
    
    new_tags, existing_tags = create_tag_objects(user, tag_list)
    update_tag_set(task_object, new_tags + existing_tags)
    task_object.save()
    return task_object
    
def update_task_description(user, new_description, task_object, \
                            tag_list = None):
    task_object.description = new_description
    
    # Try to remove this function and use tag_list obtained from client instead
    tag_list = find_tags(task_object.name + " " + new_description)
    
    new_tags, existing_tags = create_tag_objects(user, tag_list)
    update_tag_set(task_object, new_tags + existing_tags)
    task_object.save()
    return task_object
    
def update_tag_set(task_object, latest_tags):
    '''
    Takes input a task object and a list of the latest tags.
    All the task's tags have to be replaced by the new tags. This function
    deletes the task's old tags, and adds the new ones
    '''
    to_be_deleted = list(set(task_object.tags.all()) - set(latest_tags))
    to_be_added = list(set(latest_tags) - set(task_object.tags.all()))
    task_object.tags.remove(*to_be_deleted)
    task_object.tags.add(*to_be_added)

def get_task_name(user, task_id):
    return Task.objects.get(user = user, id = task_id).name

def get_description(user, task_id):
    return Task.objects.get(user = user, id = task_id).description

def get_start_date(user, task):
    return get_datetime_str(user, task.start_date)

def get_due_date(user, task):
    return get_datetime_str(user, task.due_date)

def get_closed_date(user, task):
    return get_datetime_str(user, task.closed_date)

def get_last_modified_date(user, task):
    return get_datetime_str(user, task.last_modified_date)

def get_tags(task):
    return task.tags.all()

def get_subtasks(task):
    return task.subtasks.all()

def get_parents(task):
    return task.task_set.all()

def print_task_tree(task):
    print str(task.id) + " " + task.name + "\n\t",
    subtasks = get_subtasks(task)
    for task in subtasks:
        print str(task.id) + " " + task.name
        print_task_tree(task)
        
def get_all_parents(task):
    print str(task.id) + " " + task.name + "\n\t",
    parents = get_parents(task)
    for task in parents:
        print str(task.id) + " " + task.name
        get_all_parents(task)

def set_visited(task, visited_list):
    visited_list.append(task)
    return visited_list

def visited(task, visited_list):
    return task in visited_list

def change_task_status(user, task_id, new_status):
    task = get_task_object(user, task_id)
    task.status = new_status
    
    if new_status != IS_ACTIVE:
        task.closed_date = get_current_datetime_object()
    
    task.save()
    return task

def change_task_tree_status(task, new_status):
    task.subtasks.all().update(status = new_status)
    task.save()
    for subtask in task.subtasks.all():
        change_task_tree_status(subtask, new_status)

def change_task_date(user, task_id, new_date_object, date_type):
    task = get_task_object(user, task_id)
    
    if date_type == IS_START_DATE:
        task.start_date = new_date_object
    elif date_type == IS_DUE_DATE:
        task.due_date = new_date_object
    task.save()
    return task

def change_task_tree_due_date(task, new_date_object):
    for subtask in task.subtasks.all():
        if subtask.due_date == None:
            subtask.due_date = new_date_object
        elif subtask.due_date.replace(tzinfo = None) > new_date_object:
            subtask.due_date = new_date_object
        change_task_tree_due_date(subtask, subtask.due_date)
