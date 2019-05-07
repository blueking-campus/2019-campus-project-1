# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

urlpatterns = patterns(
    'organization.views',
    (r'^$', 'get_organization_list'),
    (r'^api/new_organization/', 'new_organization'),
    (r'^api/update_organization/', 'update_organization'),
    (r'^api/delete_organization/', 'delete_organization'),
    (r'^api/get_organization/', 'get_organization')
)
