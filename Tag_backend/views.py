# Create your views here.

import json,sys

from django.http import HttpResponse, HttpResponseRedirect

from Task_backend.models import Task
from Task_backend.task import get_tasks_by_tag
from Tag_backend.tag import get_tags_by_user, delete_tag_modify_tasks, \
                            update_tag_color, update_tag_icon
from Tools.constants import *

def get_all_tags(request):
    tags = get_tags_by_user(request.user)
    return HttpResponse(json.dumps(tags, indent=4), \
                        mimetype="application/json")

def get_tasks(request):
    tag_name = request.GET.get('tag_name', '')
    folder = request.GET.get('folder', 'Active')
    
    folder_dict = {
        'All': -1,
        'Active': IS_ACTIVE,
        'Done': IS_DONE,
        'Dismissed': IS_DISMISSED
    }
    task_status = folder_dict.get(folder, IS_ACTIVE)
    
    tasks_by_tag = get_tasks_by_tag(request.user, tag_name, task_status)
    return HttpResponse(json.dumps(tasks_by_tag, indent=4), \
                        mimetype="application/json")

def add_tag(request):
    tag_id = request.GET.get('tag_id', -1)
    task_id = request.GET.get('task_id', -1)

def delete_tag(request):
    tag_name = request.GET.get('tag_name', '')
    delete_tag_modify_tasks(request.user, tag_name)
    return HttpResponseRedirect('/tags/all/')

def modify_color(request):
    tag_name = request.GET.get('tag_name', '')
    new_color = request.GET.get('new_color', '')
    folder = request.GET.get('folder', 'Active')
    update_tag_color(request.user, tag_name, new_color)
    return HttpResponseRedirect('/tags/get_tasks/?tag_name=' +
                                tag_name + '&folder=' + folder)

def modify_icon(request):
    tag_id = request.GET.get('tag_id', -1)
    new_icon = request.GET.get('icon', '')
    update_tag_icon(request.user, tag_id, new_icon)
    return HttpResponseRedirect('/tags/all/')
