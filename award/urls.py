# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    "award.views",
    (r'^$', 'index'),
    (r'^create', 'create'),
    (r'^api/create_award/', 'create_award'),
)
