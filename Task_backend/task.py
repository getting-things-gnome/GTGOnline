from Task_backend.models import Task
from User_backend.user import get_user_object
from Tag_backend.tag import find_tags, create_tag_objects
from Tools.constants import *
from Tools.dates import get_datetime_object, get_datetime_str

def get_task_object(user, task_id):
    return Task.objects.get(user = user, id = task_id)
    
def get_tasks(username):
    return Task.objects.filter(user = username)

def add_task(user, name, description = "", start_date = None, \
             due_date = None, tag_list = None):
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
    return new_task

def get_task_details(user, task_id):
    task = get_task_object(user, task_id)
    start_date = get_datetime_str(user, task.start_date)
    due_date = get_datetime_str(user, task.due_date)
    return (task.name, task.description, start_date, due_date, \
            task.tags.all(), task.subtasks.all(), task.task_set.all())

def update_task_name(user, new_name, task_object = None, task_id = None, \
                     tag_list = None):
    if task_object == None:
        task_object = get_task_object(user, task_id)
    task_object.name = new_name
    
    # Try to remove this function and use tag_list obtained from client instead
    tag_list = find_tags(new_name + " " + description)
    
    new_tags, existing_tags = create_tag_objects(user, tag_list)
#    >>> a = [1,2,3]
#>>> b = [2,3,4,5]
#>>> list(set(a) - set(b))
#[1]
#>>> list(set(b) - set(a))
#[4, 5]

    
    task_object.tags.all()
    task_object.save()
    return task_object
    
def update_task_description(user, new_description, task_object = None, \
                            task_id = None):
    if task_object == None:
        task_object = get_task_object(user, task_id)
    task_object.description = new_description
    task_object.save()
    return task_object
    
def get_task_name(user, task_id):
    return Task.objects.get(user = user, id = task_id).name

def get_task_description(user, task_id):
    return Task.objects.get(user = user, id = task_id).description

def get_task_start_date(user, task_id):
    start_date = get_task_object(user, task_id).start_date
    return get_datetime_str(user, start_date)

def get_task_due_date(user, task_id):
    due_date = get_task_object(user, task_id).due_date
    return get_datetime_str(user, due_date)

def get_task_closed_date(user, task_id):
    closed_date = get_task_object(user, task_id).closed_date
    return get_datetime_str(user, closed_date)

def get_task_last_modified_date(user, task_id):
    last_modified_date = get_task_object(user, task_id).last_modified_date
    return get_datetime_str(user, last_modified_date)

def get_task_tags(user, task_id):
    task = get_task_object(user, task_id)
    return task.tags.all()

def get_task_subtasks(user, task_id):
    task = get_task_object(user, task_id)
    return task.subtasks.all()

def get_task_parents(user, task_id):
    task = get_task_object(user, task_id)
    return task.task_set.all()


