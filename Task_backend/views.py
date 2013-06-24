# Create your views here.

import json
import sys

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required

from Task_backend.models import Task
from Task_backend.task import get_task_object, get_task_tree, \
                              change_task_status, change_task_tree_status, \
                              get_oldest_parent, delete_task_tree, add_task, \
                              get_tasks_by_due_date, update_task_details, \
                              delete_single_task, search_tasks, add_new_list
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
    
    folder_get = request.GET.get('folder', 'Active')
    folder_state = folder_dict.get(folder_get, IS_ACTIVE)
    
    if folder_state == -1:
        task_tree = get_task_tree(request.user, \
                                  Task.objects.filter(user = request.user).order_by('due_date'), \
                                  0, [], folder_state)
    else:
        task_tree = get_task_tree(request.user, \
                                  Task.objects.filter(user = request.user, \
                                                      status = folder_state).order_by('due_date'), \
                                  0, [], folder_state)
    #template = loader.get_template('task_row.html')
    #context = RequestContext(request, {'task_tree':json.dumps(task_tree)})
    #return HttpResponse(template.render(context))
    return HttpResponse(json.dumps(task_tree, indent = 4), \
                        mimetype='application/json')

@login_required
def show_title(request):
    template = loader.get_template('task_row.html')
    context = RequestContext(request, {'email': request.user.email, \
                                       'name': request.user.first_name})
    return HttpResponse(template.render(context))

def modify_status(request):
    new_status = int(request.GET.get('status', 0))
    
    if new_status < 0:
        new_status = 0
    elif new_status > 2:
        new_status = 2
    
    folder = request.GET.get('folder', 'Active')
    task_id = request.GET.get('task_id', -1)
    task_id_list = request.GET.getlist('task_id_list[]')
    if task_id_list != [] and ( task_id in task_id_list or \
                               task_id == '-1' ):
        for task_id in task_id_list:
            task = change_task_status(request.user, task_id, new_status)
            change_task_tree_status(task, new_status)
    else:
        if task_id > -1:
            task = change_task_status(request.user, task_id, new_status)
            if task != None:
                change_task_tree_status(task, new_status)
                #task_tree = get_task_tree(request.user, \
                                          #get_oldest_parent(task), \
                                          #0, [], folder)
                #return HttpResponse(json.dumps(task_tree, indent=4),
                                    #mimetype='applicatin/json')
    return HttpResponseRedirect('/tasks/get/?folder=' + folder)

def modify_date(request):
#    task_id = request.GET.get('task_id', -1)
#    if task_id < 0:
#        return HttpResponseRedirect('/tasks/get/?folder=' + folder)
#    folder = request.GET.get('folder', 'Active')
#    
#    if request.GET.has_key('start_date'):
#        new_date_object = get_datetime_object(request.GET['start_date'])
#        task = change_task_date(request.user, task_id, \
#                                new_date_object, IS_START_DATE)
#    elif request.GET.has_key('due_date'):
#        new_date_object = get_datetime_object(request.GET['due_date'])
#        task = change_task_date(request.user, task_id, \
#                                new_date_object, IS_DUE_DATE)
#        if new_date_object != None and task != None:
#            change_task_tree_due_date(task, new_date_object)
    return HttpResponseRedirect('/tasks/get/?folder=' + folder)

def delete_task(request):
    folder = request.GET.get('folder', 'Active')
    
    task_id_list = request.GET.getlist('task_id_list[]')
    if task_id_list != []:
        for task_id in task_id_list:
            task = get_task_object(request.user, task_id)
            if task != None:
                delete_task_tree(task)
                delete_single_task(task)
    else:
        task_id = request.GET.get('task_id', -1)
        if task_id != '-1':
            task = get_task_object(request.user, task_id)
            if task != None:
                delete_task_tree(task)
                delete_single_task(task)
    return HttpResponseRedirect('/tasks/get/?folder=' + folder)

def new_task(request):
    folder = request.GET.get('folder', 'Active')
    name = request.GET.get('name', 'No Name received')
    description = request.GET.get('description', '')
    start_date = request.GET.get('start_date', '')
    due_date = request.GET.get('due_date', '')
    parent_id = request.GET.get('parent_id', -1)
    
    task, parent = add_task(request.user, name, description, \
                            start_date, due_date, folder, \
                            parent_id = parent_id)
    if parent != None:
        return HttpResponse(json.dumps(task, indent=4), \
                            mimetype='application/json')
    return HttpResponseRedirect('/tasks/get/?folder=' + folder)

def update_task(request):
    folder = request.GET.get('folder', 'Active')
    name = request.GET.get('name', 'No Name received')
    description = request.GET.get('description', '')
    start_date = request.GET.get('start_date', '')
    due_date = request.GET.get('due_date', '')
    task_id = request.GET.get('task_id', -1)
    
    if task_id < 0:
        return HttpResponseRedirect('/tasks/get/?folder=' + folder)
    
    task_tree = update_task_details(request.user, task_id, name, description, \
                        start_date, due_date, folder)
    #return HttpResponseRedirect('/tasks/get/?folder=' + folder)
    #print >>sys.stderr, task_tree
    return HttpResponse(json.dumps(task_tree, indent = 4), \
                        mimetype='application/json')

def get_tasks_due_by(request):
    folder = request.GET.get('folder', 'Active')
    days_left = int(request.GET.get('days_left', 0))
    
    folder_dict = {
        'All': -1,
        'Active': IS_ACTIVE,
        'Done': IS_DONE,
        'Dismissed': IS_DISMISSED,
    }
    task_status = folder_dict[folder]
    
    due_by = request.GET.get('due_by', '0/0/0')
    tasks_list = get_tasks_by_due_date(request.user, days_left, task_status)
    return HttpResponse(json.dumps(tasks_list, indent = 4), \
                        mimetype="application/json")

def search(request):
    folder = request.GET.get('folder', 'Active')
    query = request.GET.get('query', '')
    if query == '':
        return HttpResponseRedirect('/tasks/get/?folder=' + folder)
    
    tasks_list = search_tasks(request.user, query)
    return HttpResponse(json.dumps(tasks_list, indent = 4), \
                        mimetype="application/json")

def create_new_list(request):
    folder = request.GET.get('folder', 'Active')
    new_list = request.GET.get('new_list', '')
    add_new_list(request.user, new_list, folder)
    return HttpResponseRedirect('/tasks/get/?folder=' + folder)
