#!/usr/bin/env python
from django.conf.urls import patterns, url

from Tag_backend import views

urlpatterns = patterns('',
    url(r'^all/$', views.get_all_tags, name='all'),
    url(r'^delete/$', views.delete_tag, name='delete_tag'),
)
