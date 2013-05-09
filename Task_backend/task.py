from Task_backend.models import Task
from Tag_backend.models import Tag


def get_task_object(user, task_id):
    user = get_user_object(user)
    return Task.objects.get(user = user, id = task_id)
    
def get_tasks(username):
    return Task.objects.filter(user = username)

def add_task(username, name, description = "", start_date = None, \
             due_date = None):
    new_task = Task(user = username, name = name)


