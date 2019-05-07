# -*- coding: utf-8 -*-
from sys import path

from django.conf.urls import url, patterns


urlpatterns = patterns(
    'form.views',
    (r'^$', 'get_form_list'),
    (r'^create_form/([0-9]+)/', 'create_form')
)
