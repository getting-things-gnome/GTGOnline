# Create your views here.

import json

from django.core import serializers
from django.http import HttpResponse
from django.template import loader, RequestContext

from Task_backend.models import Task
from Tag_backend.tag import find_tags

def get_serialized_tasks(request):
    all_tasks = Task.objects.all()
    data = serializers.serialize('json', all_tasks, indent = 4)
    return HttpResponse(data, mimetype='application/json')

def get_json_tasks(request):
    tasks = []
    for i in Task.objects.all():
        tasks.append({"id":i.id, "name":i.name, "description":i.description, \
        "start_date": i.start_date.strftime('%d/%m/%Y') if i.start_date != None else "", \
        "due_date":i.due_date.strftime('%d/%m/%Y') if i.due_date != None else "", \
        "status":i.get_status_display(), \
        "tags":find_tags(i.description)})
    return HttpResponse(json.dumps(tasks, indent=4), mimetype='application/json')

def show_title(request):
    template = loader.get_template('landing.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
