# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    "review.views",
    (r'^$', 'index'),
    (r'^edit_review/(?P<form_id>{[^0][0-9]*})$', 'edit_review'),
    (r'^api/reject_form/$', 'reject_form'),
    (r'^api/pass_form/$', 'pass_form'),
    (r'^api/update_review/$', 'update_review'),
)
