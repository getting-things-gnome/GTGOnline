#!/usr/bin/env python
from django.conf.urls import patterns, url

from Tag_backend import views

urlpatterns = patterns('',
    url(r'^all/$', views.get_all_tags, name='all'),
    url(r'^get_tasks/$', views.get_tasks, name='get_tasks'),
    url(r'^add/$', views.add_tag, name='add_tag'),
    url(r'^delete/$', views.delete_tag, name='delete_tag'),
    url(r'^modify/color/$', views.modify_color, name='modify_color'),
    url(r'^modify/icon/$', views.modify_icon, name='modify_icon'),
    url(r'^modify/$', views.modify_color, name='modify_color'),
    url(r'^$', views.get_all_tags, name='all'),
)
