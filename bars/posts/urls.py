# coding: utf-8

from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete
)

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^post/create/$', post_create),  # костыль
    url(ur'^(?P<id>[\w]+)$', post_detail, name='detail'),
    url(ur'^(?P<id>[\w]+)/edit/$', post_update, name='update'),
    url(ur'^(?P<id>[\w]+)/delete/$', post_delete),
]
