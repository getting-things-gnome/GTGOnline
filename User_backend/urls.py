#!/usr/bin/env python
from django.conf.urls import patterns, url

from User_backend import views

urlpatterns = patterns('',
    url(r'^landing/$', views.landing, name='landing'),
    url(r'^login/$', views.landing, name='login'),
    url(r'^authenticate/$', views.login, name='authenticate'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^after_login/$', views.after_login, name='after_login'),
    url(r'^check_email/$', views.check_email, name='check_email'),
    url(r'^register/$', views.register, name='register'),
    url(r'^search/$', views.search_user, name='search'),
    url(r'^list/$', views.get_user_list_json, name='user_list_json'),
    url(r'^$', views.landing, name='default'),
)
