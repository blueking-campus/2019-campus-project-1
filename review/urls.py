# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    "review.views",
    (r'^$', 'index'),
    (r'^api/reject_form/', 'reject_form'),
    (r'^api/pass_form/', 'pass_form'),
    (r'^edit_review/', 'edit_review'),
    (r'^api/update_review/', 'update_review'),
)
