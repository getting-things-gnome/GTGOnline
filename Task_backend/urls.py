#!/usr/bin/env python
from django.conf.urls import patterns, url

from Task_backend import views

urlpatterns = patterns('',
    url(r'^serialize/$', views.get_serialized_tasks, name='serialize'),
    url(r'^json_dumps/$', views.get_json_tasks, name='json_dumps'),
    url(r'^main/$', views.show_title, name='show_title'),
)
