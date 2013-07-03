import json

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

from Group_backend.models import Group
from Group_backend.group import create_group, delete_group, get_members, \
                                add_member_to_group, remove_member_from_group
from Tools.constants import *

def create_new_group(request):
    name = request.GET.get('name', '')
    color = request.GET.get('color', '')
    if name == '':
        name = 'No Name given'
    create_group(request.user, name, color = color)
    return HttpResponseRedirect('/groups/list/')

def delete_existing_group(request):
    name = request.GET.get('name', '')
    delete_group(request.user, name)
    return HttpResponseRedirect('/groups/list/')

def list_members_template(request):
    name = request.GET.get('name', '')
    template = loader.get_template('search_user.html')
    members = get_members(request.user, name)
    context = RequestContext(request, {'email': request.user.email, \
                                       'name': request.user.first_name, \
                                       'members': json.dumps(members), \
                                       'query': '', 'origin': 'group'})
    return HttpResponse(template.render(context))
    #return HttpResponse(json.dumps(members, indent = 4), \
                        #mimetype = "application/json")
    
def list_members(request):
    name = request.GET.get('name', '')
    members = get_members(request.user, name)
    return HttpResponse(json.dumps(members, indent = 4), \
                        mimetype = "application/json")

def add_member(request):
    name = request.GET.get('name', '')
    email = request.GET.get('email', '')
    add_member_to_group(request.user, name, email)
    return HttpResponseRedirect('/groups/list/?name=' + name)

def remove_member(request):
    name = request.GET.get('name', '')
    email = request.GET.get('email', '')
    remove_member_from_group(request.user, name, email)
    return HttpResponseRedirect('/groups/list/?name=' + name)
