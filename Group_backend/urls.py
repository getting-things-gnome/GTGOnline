#!/usr/bin/env python
from django.conf.urls import patterns, url

from Group_backend import views

urlpatterns = patterns('',
    url(r'^new/$', views.create_new_group, name='new'),
    url(r'^delete/$', views.delete_existing_group, name='delete'),
    url(r'^template/$', views.list_members_template, name='template'),
    url(r'^list/$', views.list_members, name='list'),
    url(r'^add/$', views.add_member, name='add'),
    url(r'^remove/$', views.remove_member, name='remove'),
)
