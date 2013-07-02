import json

from django.http import HttpResponse, HttpResponseRedirect

from Group_backend.models import Group
from Group_backend.group import create_group, get_members
from Tools.constants import *

def create_new_group(request):
    name = request.GET.get('name', '')
    color = request.GET.get('color', '')
    if name == '':
        name = 'No Name given'
    create_group(request.user, name, color = color)
    return HttpResponse(json.dumps(tags, indent=4), \
                        mimetype="application/json")

def list_members(request):
    name = request.GET.get('name', '')
    members = get_members(request.user, name)
    return HttpResponse(json.dumps(members, indent = 4), \
                        mimetype = "application/json")
