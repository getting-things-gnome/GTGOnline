#!/usr/bin/env python
from django.conf.urls import patterns, url
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from Api_docs import views
from User_backend.views import custom_auth_for_gtg
from Task_backend.views import new_task, bulk_update, delete_task, \
                               get_serialized_tasks
from Tag_backend.views import get_all_tags

urlpatterns = patterns('',
    url(r'^api_docs/$', views.load_api_docs, name='api_docs'),
    url(r'^user/auth/$', custom_auth_for_gtg, name='api_custom_auth'),
    url(r'^tasks/get/$', get_serialized_tasks, name='api_get_tasks'),
    url(r'^tasks/new/$', new_task, name='api_create_task'),
    url(r'^tasks/update/$', bulk_update, name='api_update_task'),
    url(r'^tasks/delete/$', delete_task, name='api_delete_task'),
    url(r'^tags/get/$', get_all_tags, name='api_get_tags'),
    url(r'^user/$', views.user_api, name='user_api'),
    url(r'^tasks/$', views.tasks_api, name='tasks_api'),
    url(r'^tags/$', views.tags_api, name='tags_api'),
    url(r'^$', views.resource_listing, name='resources'),
)
