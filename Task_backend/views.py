# Create your views here.

import json
import sys

from django.core import serializers
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from Task_backend.models import Task
from Task_backend.task import get_task_object, get_task_tree, \
                              change_task_status, change_task_tree_status, \
                              get_oldest_parent, delete_task_tree, add_task, \
                              get_tasks_by_due_date, update_task_details, \
                              delete_single_task, search_tasks, add_new_list, \
                              share_task, get_shared_task_details, \
                              get_all_tasks_details, add_gtg_tasks
from Tag_backend.tag import find_tags
from User_backend.user import authenticate_user
from Tools.constants import *
from Tools.dates import get_datetime_object

@csrf_exempt
def get_serialized_tasks(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = authenticate_user(email, password)
    if user == None:
        return HttpResponse(json.dumps([], indent = 4), \
                        mimetype='application/json')
    all_tasks = get_all_tasks_details(user)
    return HttpResponse(json.dumps(all_tasks, indent = 4), \
                        mimetype='application/json')
    
#@login_required
def get_tasks(request):
    tasks = []
    folder_dict = {
        'All': -1,
        'Active': IS_ACTIVE,
        'Done': IS_DONE,
        'Dismissed': IS_DISMISSED,
        'Your_shared_tasks': YOUR_SHARED,
        'Tasks_shared_with_you': THEY_SHARED,
    }
    
    folder_get = request.GET.get('folder', 'Active')
    folder_state = folder_dict.get(folder_get, IS_ACTIVE)
    
    if folder_state == -1:
        task_tree = get_task_tree(request.user, \
                                  request.user.task_set.all(), \
                                  0, [], folder_state)
    elif folder_state == YOUR_SHARED:
        q_set = request.user.task_set.annotate(num = Count('shared_with'))
        q_set = q_set.filter(num__gt = 0)
        task_tree = get_task_tree(request.user, q_set, \
                                  0, [], folder_state, main_list = q_set)
    elif folder_state == THEY_SHARED:
        q_set = request.user.shared_set.all()
        task_tree = get_task_tree(request.user, q_set, \
                                  0, [], folder_state, main_list = q_set)
    else:
        task_tree = get_task_tree(request.user, \
                                  request.user.task_set.filter(status = \
                                                               folder_state), \
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
    print >>sys.stderr, request.GET
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
            if task != None:
                change_task_tree_status(request.user, task, new_status)
    else:
        if task_id > -1:
            task = change_task_status(request.user, task_id, new_status)
            if task != None:
                change_task_tree_status(request.user, task, new_status)
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

@csrf_exempt
def delete_task(request):
    folder = request.GET.get('folder', 'Active')
    
    task_id_list = request.GET.getlist('task_id_list[]')
    
    query_is_from_client = True
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    if email != None and password != None:
        query_is_from_client = False
        user = authenticate_user(email, password)
        if user == None:
            return HttpResponse(json.dumps('0', indent=4), \
                                mimetype='application/json')
        task_id_list = json.loads(request.POST.get("task_id_list", ""))
    else:
        user = request.user
    
    if task_id_list != []:
        for task_id in task_id_list:
            task = get_task_object(user, task_id)
            if task != None:
                delete_task_tree(user, task)
                delete_single_task(user, task)
    else:
        task_id = request.GET.get('task_id', -1)
        print >>sys.stderr, task_id
        if task_id != '-1':
            task = get_task_object(request.user, task_id)
            if task != None:
                delete_task_tree(request.user, task)
                delete_single_task(request.user, task)
    if not query_is_from_client:
        return HttpResponse(json.dumps('1', indent=4), \
                        mimetype='application/json')
    return HttpResponseRedirect('/tasks/get/?folder=' + folder)

@csrf_exempt
def new_task(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    task_list = request.POST.get('task_list', '')
    #print >>sys.stderr, "task_list = " + str(task_list) + "type = " + str(type(task_list))
    task_list = json.loads(task_list)
    print >>sys.stderr, "task_list = " + str(task_list)
    
    user = authenticate_user(email, password)
    if user == None:
        return HttpResponse(json.dumps({}, indent=4), \
                            mimetype='application/json')
    id_dict = add_gtg_tasks(user, task_list)
    return HttpResponse(json.dumps(id_dict, indent=4), \
                            mimetype='application/json')

def update_task(request):
    folder = request.GET.get('folder', 'Active')
    name = request.REQUEST.get('name', 'No Name received')
    description = request.REQUEST.get('description', '')
    start_date = request.REQUEST.get('start_date', '')
    due_date = request.REQUEST.get('due_date', '')
    task_id = request.REQUEST.get('task_id', -1)
    origin = request.POST.get('origin', None)
    
    if origin != None:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate_user(email, password)
        update_task_details(user, task_id, name, description, \
                            start_date, due_date, folder, origin = origin)
        return HttpResponse(json.dumps('1', indent = 4), \
                            mimetype='application/json')
    
    if task_id < 0:
        return HttpResponseRedirect('/tasks/get/?folder=' + folder)
    
    task_tree = update_task_details(request.user, task_id, name, description, \
                        start_date, due_date, folder)
    #return HttpResponseRedirect('/tasks/get/?folder=' + folder)
    #print >>sys.stderr, task_tree
    return HttpResponse(json.dumps(task_tree, indent = 4), \
                        mimetype='application/json')

@csrf_exempt
def bulk_update(request):
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    user = authenticate_user(email, password)
    
    if user == None:
        return HttpResponse(json.dumps('0', indent = 4), \
                            mimetype='application/json')
    
    task_list = json.loads(request.POST.get('task_list', []))
    print >>sys.stderr, "Task List = " + str(task_list)
    for task in task_list:
        print >>sys.stderr, "STATUS = " + str(FOLDER_STATUS_INT.get(task["status"], IS_ACTIVE))
        update_task_details(user, task["task_id"], task["name"], \
                            task["description"], task["start_date"], \
                            task["due_date"], 'Active', origin = SERVICE, \
                            subtask_ids = task["subtask_ids"], \
                    status = FOLDER_STATUS_INT.get(task["status"], IS_ACTIVE))
    
    return HttpResponse(json.dumps('1', indent = 4), \
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

@csrf_exempt
def create_new_list(request):
    folder = request.POST.get('folder', 'Active')
    parent_id = request.POST.get('parent_id', -1)
    #print >>sys.stderr, 'parent id = ' + str(parent_id)
    received_list = json.loads(request.POST.get('new_list', '[]'))
    #print >>sys.stderr, received_list
    if received_list != []:
        #origin = request.POST.get('origin', None)
        #if origin != None:
            #id_dict = add_new_list(request.user, received_list, \
                                   #folder, parent_id, origin = origin)
            #return HttpResponse(json.dumps(id_dict, indent = 4), \
                                #mimetype = 'application/json')
        task = add_new_list(request.user, received_list, folder, parent_id)
        if task != None:
            return HttpResponse(json.dumps(task, indent = 4), \
                                mimetype = 'application/json')
    return HttpResponseRedirect('/tasks/get/?folder=' + folder)

@csrf_exempt
def share(request):
    folder = request.POST.get('folder', 'Active')
    task_id = request.POST.get('id', -1)
    user_list = request.POST.getlist('list[]')
    task = share_task(request.user, task_id, user_list, folder)
    if task != None:
        return HttpResponse(json.dumps(task, indent = 4), \
                            mimetype = 'application/json')
    return HttpResponseRedirect('tasks/get/?folder=' + folder)

def get_details(request):
    task_id = request.GET.get('id', -1)
    get_log = request.GET.get('log', '0')
    
    task = get_task_object(request.user, task_id)
    details = []
    if task != None and task.shared_with.exists():
        details = get_shared_task_details(task)
    return HttpResponse(json.dumps(details, indent = 4), \
                        mimetype = 'application/json')
