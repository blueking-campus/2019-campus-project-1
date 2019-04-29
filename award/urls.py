# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    "award.views",
    (r'^$', 'index'),
    (r'^create', 'create'),
    (r'^api/create_award/', 'create_award'),
    (r'^api/get_award/', 'get_award'),
    (r'^api/delete_award/', 'delete_award'),
    (r'^api/edit_award/', 'edit_award'),
    (r'^api/update_award/', 'update_award'),
)
