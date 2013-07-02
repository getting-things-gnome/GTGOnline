#!/usr/bin/env python
from django.conf.urls import patterns, url

from Group_backend import views

urlpatterns = patterns('',
    url(r'^new/$', views.create_new_group, name='new'),
    url(r'^list/$', views.list_members, name='list'),
)
