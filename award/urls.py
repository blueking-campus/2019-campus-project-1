# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    "award.views",
    (r'^$', 'index'),
    (r'^create', 'create'),
    (r'^clone_award/', 'clone_award'),
    (r'^api/create_award/', 'create_award'),
    (r'^api/get_award/', 'get_award'),
    (r'^api/search_award/', 'search_award'),
    (r'^api/delete_award/', 'delete_award'),
    (r'^api/edit_award/', 'edit_award'),
    (r'^api/update_award/', 'update_award'),
    (r'^api/clone_preview/', 'clone_preview'),
    (r'^api/clone_award/info', 'clone_award_info'),
    (r'^api/clone_award/edit_award', 'edit_clone_award'),
    # (r'^api/clone_award/delete_award', 'delete_clone_award'),
)
