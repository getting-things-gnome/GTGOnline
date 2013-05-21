#!/usr/bin/env python
from django.conf.urls import patterns, url

from User_backend import views

urlpatterns = patterns('',
    url(r'^landing/$', views.landing, name='landing'),
    url(r'^login/$', views.login, name='login'),
    url(r'^after_login/$', views.after_login, name='after_login'),
    url(r'^check/$', views.check, name='check'),
    url(r'^register/$', views.register, name='register'),
    url(r'^$', views.landing, name='default'),
)
