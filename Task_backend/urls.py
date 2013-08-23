#!/usr/bin/env python
from django.conf.urls import patterns, url

from Task_backend import views

urlpatterns = patterns('',
    url(r'^serial/$', views.get_serialized_tasks, name='serialize'),
    url(r'^get/due_by/$', views.get_tasks_due_by, name='get_tasks_due_by'),
    url(r'^get/$', views.get_tasks, name='get_tasks'),
    url(r'^update/$', views.update_task, name='update_task'),
    url(r'^bulk_update/$', views.bulk_update, name='bulk_update'),
    url(r'^modify/status/$', views.modify_status, name='modify_status'),
    url(r'^modify/date/$', views.modify_date, name='modify_date'),
    url(r'^share/$', views.share, name='share'),
    url(r'^delete/$', views.delete_task, name='delete_task'),
    url(r'^main/$', views.show_title, name='main'),
    url(r'^new/$', views.new_task, name='new_task'),
    url(r'^search/$', views.search, name='search'),
    url(r'^new_list/$', views.create_new_list, name='new_list'),
    url(r'^details/$', views.get_details, name='details'),
    url(r'^$', views.show_title, name='show_title'),
)
