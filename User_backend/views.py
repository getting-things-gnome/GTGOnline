# Create your views here.

import sys

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

from User_backend.user import register_user, login_user, logout_user
from Tools.constants import *

def landing(request):
    template = loader.get_template('landing.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def login(request):
    response = login_user(request)
    if response == USER_LOGGED_IN:
        return HttpResponseRedirect('/tasks/main/')
    elif response == USER_ACCOUNT_DISABLED:
        return 'Account has been disabled'
    else:
        return 'Invalid Login'

def logout(request):
    logout_user(request)
    print >>sys.stderr, "User logout successful"
    return HttpResponseRedirect('/user/landing/')

def after_login(request):
    template = loader.get_template('after_login.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def check(request):
    #print >>sys.stderr, "User = " + str(request.user)
    return HttpResponseRedirect('/user/landing/')

def register(request):
    if request.method == 'POST':
        #print >>sys.stderr, "register user request has been identified as POST"
        #print >>sys.stderr, "Username = " + request.POST['username']
        #print >>sys.stderr, "Email = " + request.POST['email']
        #print >>sys.stderr, "First Name = " + request.POST['first_name']
        #print >>sys.stderr, "Last Name = " + request.POST['last_name']
        #print >>sys.stderr, "Password = " + request.POST['password']
        register_user(request.POST['username'], request.POST['email'], \
                      request.POST['password'], request.POST['first_name'], \
                      request.POST['last_name']) 
    else:
        print >>sys.stderr, "request is not POST"
    return HttpResponseRedirect('/user/landing/')
