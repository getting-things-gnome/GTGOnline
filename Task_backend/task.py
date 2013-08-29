# -*- coding: utf-8 -*-

import json
import sys
import re

from django.db.models import Count

from Task_backend.models import Task, Log
from User_backend.user import get_user_object, get_user_details, \
                              get_bulk_users
from Tag_backend.tag import find_tags, create_tag_objects, get_tags_by_task, \
                            delete_orphan_tags, get_tag_object
from Tools.constants import *
from Tools.dates import get_datetime_object, get_datetime_str, \
                        get_current_datetime_object, compare_dates, \
                        get_datetime_from_days_left, get_time_now


def get_task_object(user, task_id):
    try:
        task = Task.objects.get(id = task_id)
        if user != task.user:
            if user not in task.shared_with.all():
                return None
        return task
    except Task.DoesNotExist:
        return None
    
def get_log_object(task):
    try:
        return Log.objects.get(task = task)
    except Log.DoesNotExist:
        return None
    
def get_tasks(username):
    if user != None:
        return Task.objects.filter(user = user)
    else:
        return []

def add_task(user, name, description, start_date, due_date, folder, \
             tag_list = None, parent_id = -1, parent_object = None, \
             needs_task_dict = True):
    '''
    Use this to add a new task. New task means completely new.
    Updating name, description etc. has got it's own functions.
    To create the task as a subtask, give the parent's id in parent_id
    '''
    start_date = get_datetime_object(start_date)
    due_date = get_datetime_object(due_date)
    #print >>sys.stderr, "due_date start = " + str(due_date)
    
    if start_date != None and due_date != None:
        if start_date > due_date:
            start_date = due_date
    
    new_task = Task(user = user, name = name, description = description, \
                    start_date = start_date, due_date = due_date)
    
    # Try to remove this function and use tag_list obtained from client instead
    tag_list = find_tags(name + " " + description)
    
    new_tags, existing_tags = create_tag_objects(user, tag_list)
    new_task.save()
    #print >>sys.stderr, 'after saving in add task, new_task = ' + str(new_task)
    new_task.tags.add(*(new_tags+existing_tags))
    
    parent = None
    if parent_object != None:
        parent = parent_object
    elif parent_id != -1:
        parent = get_task_object(user, parent_id)
    if parent != None:
        new_task.task_set.add(parent)
        modify_parents_dates(new_task, parent, due_date)
        if needs_task_dict:
            new_task = get_task_tree(user, get_oldest_parent(parent), \
                                     0, [], folder)
    
    #print >>sys.stderr, 'before return in add task, new_task = ' + str(new_task)        
    return new_task, parent

def modify_parents_dates(task, parent, new_due_date):
    if parent.due_date == None:
        return None
    elif new_due_date == None:
        task.due_date = parent.due_date
        task.save()
        return None
    #if new_due_date == None and parent.due_date == None:
        #oldest_parent = get_oldest_parent(parent)[0]
        #oldest_parent.due_date = new_due_date
        #oldest_parent.save()
        #set_task_tree_dates(oldest_parent, new_due_date)
        #return oldest_parent
    elif parent.due_date < new_due_date:
        parent.due_date = new_due_date
        parent.save()
        change_parents_due_dates(parent)
        return None

def set_task_tree_dates(task, new_due_date):
    all_subtasks = task.subtasks.all()
    all_subtasks.update(due_date = new_due_date)
    for index, subtask in enumerate(all_subtasks):
        set_task_tree_dates(subtask, new_due_date)

def change_parents_due_dates(task):
    if not task.task_set.exists():
        return
    for index, parent in enumerate(task.task_set.all()):
        result = compare_dates(parent.due_date, task.due_date)
        if result[0] == 1 and result[1] == 0:
            parent.due_date = task.due_date
            parent.save()
            change_parents_due_dates(parent)

def get_task_details(user, task, include_subtasks = False):
    '''
    Takes input an user object and a task object, and returns a dictionary of
    only the details of that particular task. 'subtasks' key will be set to
    empty list, and 'indent' key will be set to 0.
    This dictionary can then be appended to the JSON object.
    User object is needed to get the datetime in string format based on his
    preferences
    '''
    start_date = get_datetime_str(user, task.start_date)
    due_date = get_datetime_str(user, task.due_date)
    closed_date = get_datetime_str(user, task.closed_date)
    last_modified_date = get_datetime_str(user, task.last_modified_date, \
                                          precise_needed = True)
    subtask_list = []
    if include_subtasks:
        subtask_list = [str(subtask.id) for subtask in task.subtasks.all()]
    details =  {"id": task.id, "name": task.name, \
                "description": task.description, \
                "start_date": start_date, "due_date": due_date, \
                "closed_date": closed_date, \
                "last_modified_date": last_modified_date, \
                "status": task.status, "tags": get_tags_by_task(task), \
                "subtasks": subtask_list, "indent": 0, \
                "shared_with": [], "owner": ''}
    return details

def get_task_tree_details(user, task, indent, visited_list, folder, \
                          main_list=[]):
    '''
    Takes input an user object and a task object, and returns a dictionary of all
    the details for the task AND all of it's subtasks having the same status.
    This dictionary can then be appended to the JSON object.
    User object is needed to get the datetime in string format based on his
    preferences
    '''
    
    start_date = get_datetime_str(user, task.start_date)
    due_date = get_datetime_str(user, task.due_date)
    closed_date = get_datetime_str(user, task.closed_date)
    last_modified_date = get_datetime_str(user, task.last_modified_date)
    
    shared = [get_user_details(i) for i in task.shared_with.all()]
    owner = ''
    
    if folder == -1:
        subtasks_list = task.subtasks.all()
    elif folder == YOUR_SHARED:
        subtasks_list = task.subtasks.annotate(num = Count('shared_with'))
        subtasks_list = subtasks_list.filter(num__gt = 0)
        print >>sys.stderr, "subtasks found = " + str(subtasks_list)
        owner = get_user_details(task.user)
    elif folder == THEY_SHARED:
        q = list(set(task.subtasks.all()).intersection(user.shared_set.all()))
        subtasks_list = q
        shared = []
        owner = get_user_details(task.user)
    else:
        subtasks_list = task.subtasks.filter(status = task.status)
        
    details =  {"id": task.id, "name": task.name, \
                "description": task.description, \
                "start_date": start_date, "due_date": due_date, \
                "closed_date": closed_date, \
                "last_modified_date": last_modified_date, \
                "status": task.status, "tags": get_tags_by_task(task), \
                "subtasks": get_task_tree(user, subtasks_list, \
                                          indent+1, visited_list, folder, \
                                          main_list = main_list), \
                "shared_with": shared, "owner": owner, \
                "indent": indent}    
    return details

def get_task_tree(user, task_list, indent, visited_list, folder, main_list=[]):
    task_tree = []
    print >>sys.stderr, 'task_list = ' + str(task_list)
    for index, task in enumerate(task_list):
        # The following condition will have to changed in the future
        # to enable tasks with multiple parents
        # Detailed explanation -
        parent = get_parent(task)
        if not visited(task, visited_list) and ( not task.task_set.exists() \
                or visited(parent, visited_list) \
                or (task.status != get_parent_status(task) and \
                    folder != -1 ) or ((folder == YOUR_SHARED or \
                                         folder == THEY_SHARED)) and \
                parent not in main_list): # problem here
            print >>sys.stderr, 'visiting = ' + str(task)
            visited_list = set_visited(task, visited_list)
            task_tree.append(get_task_tree_details(user, task, indent, \
                                                   visited_list, folder, \
                                                   main_list = main_list))
    return task_tree

def any_parent_visited(task, obj_list):
    if task in obj_list:
        return True
    parent = get_parent(task)
    if parent == None:
        return False
    return any_parent_visited(parent, obj_list)

def get_shared_task_tree(user, task_list, indent, visited_list, folder):
    task_tree = []
    print >>sys.stderr, 'task_list = ' + str(task_list)
    while list(task_list) != []:
        parent = check_any_parent_in_list(task, task_list)
        if parent == None:
            if not visited(task, visited_list):
                visited_list = set_visited(task, visited_list)
                task_tree.append(get_task_details(user, task))
                task_list.remove(task)
        else:
            if not visited(parent, visited_list):
                continue
        if not visited(task, visited_list) and ( not task.task_set.exists() \
                or visited(get_parent(task), visited_list) \
                or ( task.status != get_parent_status(task) and \
                     folder != -1 ) or ((folder == YOUR_SHARED or \
                                         folder == THEY_SHARED) and \
                    visited(get_oldest_parent(task), visited_list))):
            print >>sys.stderr, 'visiting = ' + str(task)
            visited_list = set_visited(task, visited_list)
            task_tree.append(get_task_tree_details(user, task, \
                                              indent, visited_list, folder))
    return task_tree

def check_any_parent_in_list(task, obj_list):
    if task.task_set.exists():
        parent = task.task_set.all()[0]
        if parent in obj_list:
            return parent
        return check_any_parent_in_list(parent, obj_list)
    return None

def get_task_tree2(user, task_list, indent, visited_list, folder):
    task_tree = []
    for index, task in enumerate(task_list):
        if not visited(task, visited_list):
            visited_list = set_visited(task, visited_list)
            oldest_parent = get_oldest_parent(task)

def update_task_details(user, task_id, new_name, new_description, \
                        new_start_date, new_due_date, folder, \
                        origin = None, subtask_ids = []):
    task = get_task_object(user, task_id)
    if task == None:
        return
    task.name = new_name
    task.description = new_description
    
    tag_list = find_tags(new_name + " " + new_description)
    new_tags, existing_tags = create_tag_objects(user, tag_list)
    update_tag_set(task, new_tags + existing_tags)
    
    new_start_date = get_datetime_object(new_start_date)
    task = change_task_date(user, task, new_start_date, IS_START_DATE)
    new_due_date = get_datetime_object(new_due_date)
    task = change_task_date(user, task, new_due_date, IS_DUE_DATE)
    
    if task.shared_with.exists():
        update_log(user, task, LOG_TASK_MODIFY)
    
    if subtask_ids != []:
        task = add_remove_subtasks(task, subtask_ids)
    
    change_task_tree_due_date(user, task, new_due_date)
    task.save()
    #print >>sys.stderr, str(get_oldest_parent(task))
    
    if origin != None:
        return None
    
    return get_task_tree(user, get_oldest_parent(task), 0, [], folder)

def add_remove_subtasks(task, subtask_ids):
    existing = task.subtasks.all()
    existing_ids = [str(subtask.id) for subtask in existing]
    print >>sys.stderr, "Subtask ids = " + str(subtask_ids)
    print >>sys.stderr, "Existing Subtask ids = " + str(existing_ids)
    to_add = list(set(subtask_ids) - set(existing_ids))
    
    to_add_tasks = Task.objects.filter(id__in = to_add)
    print >>sys.stderr, "To Add subtasks = " + str(to_add_tasks)
    task.subtasks.add(*to_add_tasks)
    
    to_delete = list(set(existing_ids) - set(subtask_ids))
    to_delete_tasks = task.subtasks.filter(id__in = to_delete)
    print >>sys.stderr, "To Delete subtasks = " + str(to_delete_tasks)
    task.subtasks.remove(*to_delete_tasks)
    
    return task

#def update_task_name(user, new_name, task_object, tag_list = None):
#    task_object.name = new_name
#    
#    # Try to remove this function and use tag_list obtained from client instead
#    tag_list = find_tags(new_name + " " + task_object.description)
#    
#    new_tags, existing_tags = create_tag_objects(user, tag_list)
#    update_tag_set(task_object, new_tags + existing_tags)
#    task_object.save()
#    return task_object
#    
#def update_task_description(user, new_description, task_object, \
#                            tag_list = None):
#    task_object.description = new_description
#    
#    # Try to remove this function and use tag_list obtained from client instead
#    tag_list = find_tags(task_object.name + " " + new_description)
#    
#    new_tags, existing_tags = create_tag_objects(user, tag_list)
#    update_tag_set(task_object, new_tags + existing_tags)
#    task_object.save()
#    return task_object
    
def update_tag_set(task_object, latest_tags):
    '''
    Takes input a task object and a list of the latest tags.
    All the task's tags have to be replaced by the new tags. This function
    deletes the task's old tags, and adds the new ones
    '''
    to_be_deleted = list(set(task_object.tags.all()) - set(latest_tags))
    to_be_added = list(set(latest_tags) - set(task_object.tags.all()))
    task_object.tags.remove(*to_be_deleted)
    delete_orphan_tags(task_object, to_be_deleted)
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

def get_parent(task):
    if task.task_set.exists():
        return task.task_set.all()[0]
    else:
        return None

def get_parent_status(task):
    parent = get_parent(task)
    if parent == None:
        return None
    else:
        return parent.status

def get_oldest_parent(task):
    if task.task_set.exists():
        # Note that this only works because we are assuming that a task
        # only has ONE parent
        return get_oldest_parent(task.task_set.all()[0])
    else:
        # List is returned because get_task_tree function accepts only lists
        return [task]

def print_task_tree(task):
    #print str(task.id) + " " + task.name + "\n\t",
    subtasks = get_subtasks(task)
    for task in subtasks:
        #print str(task.id) + " " + task.name
        print_task_tree(task)
        
def get_all_parents(task):
    #print str(task.id) + " " + task.name + "\n\t",
    parents = get_parents(task)
    for task in parents:
        #print str(task.id) + " " + task.name
        get_all_parents(task)

def set_visited(task, visited_list):
    visited_list.append(task)
    return visited_list

def visited(task, visited_list):
    return task in visited_list

def change_task_status(user, task_id, new_status):
    task = get_task_object(user, task_id)
    if task == None:
        return None
    task.status = new_status
    
    if new_status == IS_ACTIVE:
        task.closed_date = None
    else:
        task.closed_date = get_current_datetime_object()
    
    task.save()
    if task.shared_with.exists():
        update_log(user, task, LOG_TASK_STATUS, new_status = new_status)
    return task

def change_task_tree_status(user, task, new_status):
    if new_status == IS_ACTIVE:
        new_closed_date = None
    else:
        new_closed_date = get_current_datetime_object()
    task.subtasks.all().update(status = new_status, \
                               closed_date = new_closed_date)
    for index, subtask in enumerate(task.subtasks.all()):
        if subtask.shared_with.exists():
            update_log(user, subtask, LOG_TASK_STATUS, new_status = new_status)
        change_task_tree_status(user, subtask, new_status)

def change_task_date(user, task, new_date_object, date_type):
    if date_type == IS_START_DATE:
        task.start_date = new_date_object
    elif date_type == IS_DUE_DATE:
        task.due_date = new_date_object
        if task.task_set.exists():
            parent = task.task_set.all()[0]
            if new_date_object == None and parent.due_date != None:
                task.due_date = parent.due_date
            
    compare_result = compare_dates(task.start_date, task.due_date)
    if compare_result[0] and compare_result[1]:
        task.start_date = task.due_date
    task.save()
    return task

def change_task_tree_due_date(user, task, new_date_object):
    if new_date_object != None:
        update_children_due_date(user, task, new_date_object)
    update_parent_due_date(user, task, new_date_object)
    
def update_children_due_date(user, task, new_date_object):
    for index, subtask in enumerate(task.subtasks.all()):
        #print >>sys.stderr, "updating subtask = " + subtask.name
        if subtask.due_date == None or \
            subtask.due_date.replace(tzinfo = None) > new_date_object:
            #print >>sys.stderr, "subtask due date replaced = " + str(new_date_object)
            subtask.due_date = new_date_object
            
            dates_diff = compare_dates(subtask.start_date, subtask.due_date)
            if dates_diff[0] and dates_diff[1]:
                #print >>sys.stderr, "subtask start date replaced = " + str(new_date_object)
                subtask.start_date = subtask.due_date
            update_log(user, subtask, LOG_TASK_MODIFY)
        subtask.save()
        update_children_due_date(user, subtask, subtask.due_date)

def update_parent_due_date(user, task, new_date_object):
    for index, parent in enumerate(task.task_set.all()):
        #print >>sys.stderr, "updating parent = " + parent.name + " due date = " + str(parent.due_date)
        if parent.due_date != None:
            if new_date_object == None:
                #print >>sys.stderr, "task due date replaced = " + str(new_date_object)
                task.due_date = parent.due_date
            elif parent.due_date.replace(tzinfo = None) < new_date_object:
                #print >>sys.stderr, "parent due date replaced = " + str(new_date_object)
                parent.due_date = new_date_object
            
            dates_diff = compare_dates(parent.start_date, parent.due_date)
            if dates_diff[0] and dates_diff[1]:
                #print >>sys.stderr, "parent start date replaced = " + str(new_date_object)
                parent.start_date = parent.due_date
            update_log(user, parent, LOG_TASK_MODIFY)
        parent.save()
        update_parent_due_date(user, parent, parent.due_date)

def delete_single_task(user, task):
    tags_list = task.tags.all()
    delete_orphan_tags(task, tags_list)
    if task.shared_with.exists():
        update_log(user, task, LOG_TASK_DELETE)
    task.delete()
    #print >>sys.stderr, "after delete, tags_list = " + str(tags_list)

def delete_task_tree(user, task):
    for index, subtask in enumerate(task.subtasks.all()):
        if subtask.subtasks.exists():
            delete_task_tree(user, subtask)
        tags_list = subtask.tags.all()
        delete_orphan_tags(subtask, tags_list)
        if subtask.shared_with.exists():
            update_log(user, subtask, LOG_TASK_DELETE)
        subtask.delete()
        #print >>sys.stderr, "after delete, tags_list = " + str(tags_list)

def get_tasks_by_tag(user, tag_name, task_status):
    tag = get_tag_object(user, tag_name = tag_name)
    print >>sys.stderr, "tag name = " + tag.name + "user = " + user.email + "status = " + str(task_status)
    if tag == None:
        return []
    task_list = []
    if task_status == -1:
        query_set = tag.task_set.all()
    else:
        query_set = tag.task_set.filter(status = task_status)
    for task in query_set:
        task_list.append(get_task_details(user, task))
    print >>sys.stderr, "task = " + str(task_list)
    return task_list

def get_tasks_by_due_date(user, days_left, task_status):
    task_list = []
    datetime_object = get_datetime_from_days_left(days_left)
    tasks = Task.objects.filter(user = user, due_date = datetime_object, \
                                status = task_status)
    for task in tasks:
        task_list.append(get_task_details(user, task))
    return task_list

def search_tasks(user, query):
    tasks = Task.objects.filter(user = user, name__icontains = query)
    task_list = []
    for task in tasks:
        task_list.append(get_task_details(user, task))
    return task_list

def add_new_list(user, new_list, folder, parent_id):
    #print >>sys.stderr, new_list
    created_tasks = {}
    for task in new_list:
        level = int(task.get('level', '0'))
        if level == 0:
            #print >>sys.stderr, 'main task creation started, ' + str(created_tasks)
            new_task, parent = add_task(user, \
                        task.get('name', 'No name provided'), \
                        task.get('description', 'none'), \
                        task.get('start_date', ''), task.get('due_date', ''), \
                        folder, parent_id = parent_id, needs_task_dict = False)
        else:
            #print >>sys.stderr, 'subtask creation started, ' + str(created_tasks) + ' level = ' + str(level)
            new_task, parent = add_task(user, \
                        task.get('name', 'No name provided'), \
                        task.get('description', 'none'), \
                        task.get('start_date', ''), task.get('due_date', ''), \
                        folder, \
                        parent_object = created_tasks.get(level-1, None), \
                        needs_task_dict = False)
        #print >>sys.stderr, 'new task = ' + str(new_task)
        created_tasks[level] = new_task
        #if origin != None:
            #id_dict[task.get('gtg_id', 'None')] = new_task.id
            #new_task.status = FOLDER_STATUS_INT[task.get('status', 'Active')]
            #new_task.save()
        print >>sys.stderr, "new task = " + str(new_task) + "parent = " + str(parent)
        #update_log(new_task, LOG_NEW_TASK)
    
    #if origin != None:
        #print >>sys.stderr, "Id dict = " + str(id_dict)
        #return id_dict
    
    if parent_id == '-1':
        return None
    oldest = get_oldest_parent(get_task_object(user, parent_id))
    return get_task_tree(user, oldest, 0, [], folder)

def share_task(user, task_id, email_list, folder):
    print >>sys.stderr, ' User is = ' + user.get_full_name()
    task = get_task_object(user, task_id)
    if task == None:
        return None
    
    users_obj = get_bulk_users(email_list)
    print >>sys.stderr, 'received list = ' + str(users_obj)
    update_log(user, task, LOG_TASK_SHARE, user_list = users_obj)
    add_remove_shared_users(task, users_obj)
    share_task_children(user, task, users_obj)
    
    oldest = get_oldest_parent(task)
    return get_task_tree(user, oldest, 0, [], folder)

def share_task_children(user, task, users_obj):
    for subtask in task.subtasks.all():
        add_remove_shared_users(subtask, users_obj)
        update_log(user, subtask, LOG_TASK_SHARE, user_list = users_obj)
        share_task_children(user, subtask, users_obj)

def add_remove_shared_users(task, users_obj):
    to_be_deleted = list(set(task.shared_with.all()) - set(users_obj))
    to_be_added = list(set(users_obj) - set(task.shared_with.all()))
    task.shared_with.remove(*to_be_deleted)
    task.shared_with.add(*to_be_added)

def get_shared_task_details(task):
    shared = []
    for user in task.shared_with.all():
        shared.append(get_user_details(user))
    log_obj = get_log_object(task)
    log = 'None' if log_obj == None else log_obj.log
    return { "owner": get_user_details(task.user), \
             "shared_with": shared, "log": log }

def update_log(user, task, log_type, user_list = [], new_status = IS_ACTIVE):
    if log_type == LOG_NEW_TASK:
        s = get_time_now() + ' Task created by ' + \
            task.user.get_full_name() + '\n'
        log = Log(task = task, log = s)
    elif log_type == LOG_TASK_MODIFY:
        obj, new = Log.objects.get_or_create(task = task)
        s = '1 [' + get_time_now() + '] by "' + user.get_full_name() + '"\n'
        obj.log += s
        obj.save()
    elif log_type == LOG_TASK_SHARE:
        if list(user_list) == []:
            return
        obj, new = Log.objects.get_or_create(task = task)
        names = ''
        for person in user_list:
            names += person.get_full_name() + ', '
        s = '2 [' + get_time_now() + '] "' + user.get_full_name() + \
            '" shared to ' + names[:-2] + '\n'
        obj.log += s
        obj.save()
    elif log_type == LOG_TASK_STATUS:
        obj, new = Log.objects.get_or_create(task = task)
        s = '3 [' + get_time_now() + '] "' + \
            user.get_full_name() + '" changed to ' + \
            FOLDER_STATUS_STR.get(new_status, 'Undefined') + '\n'
        obj.log += s
        obj.save()
    else:
        try:
            obj = Log.objects.get(task = task)
            obj.delete()
        except Log.DoesNotExist:
            pass

def get_all_tasks_details(email):
    user = get_user_object(email)
    if user == None:
        return []
    all_tasks = []
    for task in user.task_set.all():
        all_tasks.append(get_task_details(user, task, include_subtasks = True))
    return all_tasks

def add_gtg_tasks(user, task_list):
    subtasks = {}
    id_dict = {}
    print >>sys.stderr, "At starting, task list = " + str(task_list) + '\n\n'
    for key, value in task_list.iteritems():
        print >>sys.stderr, "key = " + key + " value = " + str(value)
        if value['subtasks'] != []:
            subtasks[key] = value['subtasks']
        task, parent = add_task(user, value['name'], value['description'], \
                                value['start_date'], value['due_date'], \
                                None, needs_task_dict = False)
        task_list[key] = task
        id_dict[key] = str(task.id)
        
    for key, value in subtasks.iteritems():
        task = task_list[key]
        to_add = []
        for gtg_id in value:
            to_add.append(task_list[gtg_id])
        task.subtasks.add(*to_add)
    
    print >>sys.stderr, "After, updated task_list = " + str(task_list)
    print >>sys.stderr, "After, updated subtasks = " + str(subtasks) + '\n\n'
    return id_dict
