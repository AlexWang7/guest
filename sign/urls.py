#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/18 13:13
# @Author  : wxn
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @Describe:

from django.conf.urls import url

from sign import views_if, views_if_sec

app_name = 'sign'
urlpatterns = [
    # guest system interface:
    # ex: /api/add_event
    url(r'^add_event', views_if.add_event, name='add_event'),
    url(r'^add_guest', views_if.add_guest, name='add_guest'),
    url(r'^get_event_list/', views_if.get_event_list, name='get_event_list'),
    url(r'^get_guest_list/', views_if.get_guest_list, name='get_guest_list'),
    url(r'^user_sign/', views_if.user_sign, name='user_sign'),
    url(r'^sec_get_event_list/',views_if_sec.get_event_list,name='get_event_list'),
]
