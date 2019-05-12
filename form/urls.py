# -*- coding: utf-8 -*-
from sys import path

from django.conf.urls import url, patterns


urlpatterns = patterns(
    'form.views',
    (r'^$', 'get_form_list'),
    (r'^create_form/([0-9]+)/', 'create_form'),
    (r'^get_form/([0-9]+)/', 'get_form'),
    (r'^update_form/([0-9]+)/', 'update_form'),
    (r'^search_form/', 'search_form')
)
