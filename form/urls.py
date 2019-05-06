# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

urlpatterns = patterns(
    'form.views',
    (r'^$', 'get_forms'),
    (r'^create_form', 'create_form')
)
