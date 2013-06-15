# Create your views here.

import sys
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import render_to_response

from User_backend.user import register_user, login_user, logout_user, \
                              validate_form, does_email_exist
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
    error_dict = {'error': errors_list.get(error, 'Unknown Error')}
    if error == '4':
        error_dict['success'] = errors_list.get(error);
        error_dict['error'] = None;
    context = RequestContext(request, error_dict)
    return HttpResponse(template.render(context))

def login(request):
    response = login_user(request)
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
        if not validate_form(email, password):
            request.session['error'] = '3'
            return HttpResponseRedirect('/user/landing/')
        register_user(email, password, \
                      request.POST['first_name'], request.POST['last_name']) 
    else:
        print >>sys.stderr, "request is not POST"
    request.session['error'] = '4'
    return HttpResponseRedirect('/user/landing/')
