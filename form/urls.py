# -*- coding: utf-8 -*-
from sys import path

from django.conf.urls import url, patterns

from form import views

urlpatterns = patterns(
    'form.views',
    (r'^$/', 'get_forms'),
    (r'^create_form/([0-9]{1,})/', 'create_form')
)
