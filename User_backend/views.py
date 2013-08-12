# Create your views here.

import sys
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from User_backend.user import register_user, login_user, logout_user, \
                              validate_form, does_email_exist, \
                              fetch_gravatar_profile
from Group_backend.group import find_users_from_query
from Group_backend.group import create_default_groups
from Tools.constants import *

def landing(request):
    template = loader.get_template('landing.html')
    
    errors_list = {
        '0': None,
        '1': 'Incorrect Email/Password combination',
        '2': 'Account has been disabled',
        '3': 'Email or Password was invalid, ' \
             'so Registration is unsuccessful, please register again',
        '4': 'Registration Successful, you may now login',
    }
    
    error = request.session.get('error', '0');
    request.session.flush()
    error_dict = {'error': errors_list.get(error, 'Unknown Error')}
    if error == '4':
        error_dict['success'] = errors_list.get(error);
        error_dict['error'] = None;
    context = RequestContext(request, error_dict)
    return HttpResponse(template.render(context))

@csrf_exempt
def login(request):
    if request.POST.get('email', '') == '':
        template = loader.get_template('landing.html')
        context = RequestContext(request, {})
        return HttpResponse(template.render(context))
    if request.POST.get('origin', '') == 'gtg':
        print >>sys.stderr, "Request is from GTG"
        return HttpResponse('1', mimetype='application/json')
    else:
        print >>sys.stderr, "Nope"
    response = login_user(request, request.POST['email'], \
                          request.POST['password'])
    if response == USER_LOGGED_IN:
        request.session['error'] = '0'
        return HttpResponseRedirect('/tasks/main/')
    elif response == USER_ACCOUNT_DISABLED:
        request.session['error'] = '2'
        return HttpResponseRedirect('/user/landing/')
    else:
        request.session['error'] = '1'
        return HttpResponseRedirect('/user/landing/')

def logout(request):
    logout_user(request)
    print >>sys.stderr, "User logout successful"
    return HttpResponseRedirect('/user/landing/')

def after_login(request):
    template = loader.get_template('after_login.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def check_email(request):
    if does_email_exist(request.GET.get('email', '')):
        print >>sys.stderr, "exists"
        return HttpResponse('1', mimetype='application/json')
    else:
        print >>sys.stderr, "not exists"
        return HttpResponse('0', mimetype='application/json')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if not validate_form(email, password, first_name, last_name):
            request.session['error'] = '3'
            return HttpResponseRedirect('/user/landing/')
        user = register_user(email, password, first_name, last_name)
        if user != None:
            create_default_groups(user)
            response = login_user(request, email, password)
            if response == USER_LOGGED_IN:
                request.session['error'] = '0'
                return HttpResponseRedirect('/tasks/main/')
    request.session['error'] = '4'
    return HttpResponseRedirect('/user/landing/')

@login_required
def search_user(request):
    query = request.GET.get('query', '')
    print >>sys.stderr, query
    template = loader.get_template('search_user.html')
    user_list = find_users_from_query(request.user, query, GROUPED)
    context = RequestContext(request, {'email': request.user.email, \
                                       'name': request.user.first_name, \
                                       'users': json.dumps(user_list), \
                                       'query': query, 'origin': 'search'})
    return HttpResponse(template.render(context))

@csrf_exempt
def get_user_list_json(request):
    query = request.POST.get('query', '')
    visited = request.POST.getlist('visited[]')
    visited.append(request.user.email)
    print >>sys.stderr, visited
    user_list = find_users_from_query(request.user, query, NON_GROUPED, \
                                      visited = visited)
    return HttpResponse(json.dumps(user_list), mimetype='application/json')

def show_user_profile(request):
    profile_email = request.GET.get('email', request.user.email)
    if profile_email == '':
        profile_email = request.user.email
    template = loader.get_template('user_profile.html')
    context = RequestContext(request, {'email': request.user.email, \
                                       'name': request.user.get_full_name(), \
                                       'profile_email': profile_email})
    return HttpResponse(template.render(context))

def get_gravatar(request):
    email = request.GET.get('email', '')
    email_hash = request.GET.get('hash', '')
    profile_obj = fetch_gravatar_profile(email, email_hash)
    if profile_obj == None:
        return HttpResponse('0', mimetype='application/json')
    profile = json.load(profile_obj)
    print >>sys.stderr, 'profile = ' + str(profile)
    return HttpResponse(json.dumps(profile), mimetype='application/json')
