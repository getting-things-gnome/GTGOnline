#!/usr/bin/env python
from django.conf.urls import patterns, url

from Task_backend import views

urlpatterns = patterns('',
    url(r'^serialize/$', views.get_serialized_tasks, name='serialize'),
    url(r'^get/$', views.get_tasks, name='get_tasks'),
    url(r'^modify/status/$', views.modify_status, name='modify_status'),
    url(r'^modify/date/$', views.modify_date, name='modify_date'),
    url(r'^delete/$', views.delete_task, name='delete_task'),
    url(r'^main/$', views.show_title, name='show_title'),
)
