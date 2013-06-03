# Create your views here.

import json

from django.http import HttpResponse, HttpResponseRedirect

from Task_backend.models import Task
from Tag_backend.tag import get_tags_by_user, delete_tag_modify_tasks, \
                            update_tag_color, update_tag_icon

def get_all_tags(request):
    tags = get_tags_by_user(request.user)
    return HttpResponse(json.dumps(tags, indent=4), \
                        mimetype="application/json")

def add_tag(request):
    tag_id = request.GET.get('tag_id', -1)
    task_id = request.GET.get('task_id', -1)

def delete_tag(request):
    tag_id = request.GET.get('tag_id', -1)
    delete_tag_modify_tasks(request.user, tag_id)
    return HttpResponseRedirect('/tags/all/')

def modify_color(request):
    tag_id = request.GET.get('tag_id', -1)
    new_color = request.GET.get('color', '')
    update_tag_color(request.user, tag_id, new_color)
    return HttpResponseRedirect('/tags/all/')

def modify_icon(request):
    tag_id = request.GET.get('tag_id', -1)
    new_icon = request.GET.get('icon', '')
    update_tag_icon(request.user, tag_id, new_icon)
    return HttpResponseRedirect('/tags/all/')
