# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'organization.views',
    url(r'^new_organization/$', 'new_organization'),
    url(r'^$', 'show_organizations'),
    url(r'^update_organization/$', 'update_organization'),
    url(r'^del_organization/$', 'del_organization'),
)
