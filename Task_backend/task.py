from Task_backend.models import Task
from Tag_backend.models import Tag
from User_backend.user import get_user_object
from Tag_backend.tag import find_tags, create_tag_objects


def get_task_object(user, task_id):
    user = get_user_object(user)
    return Task.objects.get(user = user, id = task_id)
    
def get_tasks(username):
    return Task.objects.filter(user = username)

def add_task(user, name, description = "", start_date = None, \
             due_date = None, tag_list = None):
    user = get_user_object(user)
    new_task = Task(user = user, name = name, description = description, \
                    start_date = start_date, due_date = due_date)
    
    # Try to remove this function and use tag_list obtained from client instead
    tag_list = find_tags(description)
    new_tags, existing_tags = create_tag_objects(user, tag_list)
    new_task.save()
    new_task.tags.add(*(list(new_tags)+existing_tags))
    return new_task

def update_task_name(user, new_name, task_object = None, task_id = None):
    if task_object == None:
        task_object = get_task_object(user, task_id)
    task_object.name = new_name
    task_object.save()
    
def update_task_description(user, new_description, task_object = None, \
                            task_id = None):
    if task_object == None:
        task_object = get_task_object(user, task_id)
    task_object.description = new_description
    task_object.save()

