#!/usr/bin/env python
from django.conf.urls import patterns, url

from demo import views

urlpatterns = patterns('',
    url(r'^$', views.demo, name='demo'),
    url(r'^demo/$', views.demo, name='demo'),
    url(r'^create/$', views.create, name='create'),
    url(r'^create_advanced/$', views.create_advanced, name='create_advanced'),
    url(r'^demo/(?P<task_id>\d+)/mark_done/$', views.mark_done, name='mark_done'),
    url(r'^demo/(?P<task_id>\d+)/mark_dismissed/$', views.mark_dismissed, name='mark_dismissed'),
    url(r'^demo/(?P<task_id>\d+)/mark_active/$', views.mark_active, name='mark_active'),
    url(r'^demo/(?P<task_id>\d+)/delete/$', views.delete, name='delete'),
    url(r'^advanced/$', views.advanced, name='advanced'),
)
