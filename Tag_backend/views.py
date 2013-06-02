# Create your views here.

import json

from django.http import HttpResponse, HttpResponseRedirect

from Task_backend.models import Task
from Tag_backend.tag import get_tags_by_user, delete_tag_modify_tasks

def get_all_tags(request):
    tags = get_tags_by_user(request.user)
    return HttpResponse(json.dumps(tags, indent=4), \
                        mimetype="application/json")

def delete_tag(request):
    tag_id = request.GET.get('tag_id', -1)
    if tag_id < 0:
        return HttpResponseRedirect('/tags/all/')
    
    delete_tag_modify_tasks(request.user, tag_id)
    return HttpResponseRedirect('/tags/all/')
