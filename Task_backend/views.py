# Create your views here.

import json
import sys

from django.core import serializers
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required

from Task_backend.models import Task
from Task_backend.task import get_task_tree
from Tag_backend.tag import find_tags
from Tools.constants import *
from Tools.dates import get_datetime_object

def get_serialized_tasks(request):
    all_tasks = Task.objects.all()
    data = serializers.serialize('json', all_tasks, indent = 4)
    return HttpResponse(data, mimetype='application/json')

#@login_required
def get_tasks(request):
    tasks = []
    folder_dict = {
        'All': -1,
        'Active': IS_ACTIVE,
        'Done': IS_DONE,
        'Dismissed': IS_DISMISSED,
    }
    
    folder_state = folder_dict[request.GET['folder']]
    if request.GET.has_key('due'):
        date_filter = True
        due_date = request.GET['due']
    
    if folder_state == -1:
        task_tree = get_task_tree(request.user, \
                              Task.objects.filter(user = request.user))
    else:
        task_tree = get_task_tree(request.user, \
                              Task.objects.filter(user = request.user, \
                                                  status = folder_state))
    #template = loader.get_template('task_row.html')
    #context = RequestContext(request, {'task_tree':json.dumps(task_tree)})
    #return HttpResponse(template.render(context))
    return HttpResponse(json.dumps(task_tree, indent=4), \
                        mimetype='application/json')

@login_required
def show_title(request):
    template = loader.get_template('task_row.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
