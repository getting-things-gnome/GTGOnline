#!/usr/bin/env python
from django.conf.urls import patterns, url

from Api_docs import views

urlpatterns = patterns('',
    #url(r'^landing/$', views.landing, name='landing'),
    #url(r'^login/$', views.landing, name='login'),
    #url(r'^authenticate/$', views.login, name='authenticate'),
    #url(r'^auth_gtg/$', views.custom_auth_for_gtg, name='auth_gtg'),
    #url(r'^logout/$', views.logout, name='logout'),
    #url(r'^after_login/$', views.after_login, name='after_login'),
    #url(r'^check/$', views.check_email, name='check_email'),
    #url(r'^gravatar/$', views.get_gravatar, name='get_gravatar'),
    #url(r'^register/$', views.register, name='register'),
    #url(r'^search/json/$', views.get_user_list_json, name='user_list_json'),
    #url(r'^search/$', views.search_user, name='search'),
    #url(r'^profile/$', views.show_user_profile, name='profile'),
    url(r'^$', views.resource_listing, name='resources'),
)
