# Create your views here.

import json

from django.core import serializers
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required

from Task_backend.models import Task
from Task_backend.task import get_task_tree
from Tag_backend.tag import find_tags
from Tools.constants import *

def get_serialized_tasks(request):
    all_tasks = Task.objects.all()
    data = serializers.serialize('json', all_tasks, indent = 4)
    return HttpResponse(data, mimetype='application/json')

#@login_required
def get_json_tasks(request):
    tasks = []
    task_tree = get_task_tree(request.user, \
                              Task.objects.filter(user = request.user, \
                                                  status = IS_ACTIVE))
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
