# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

urlpatterns = patterns(
    'organization.views',
    url(r'^$', 'get_organizations'),
    url(r'^api/new_organization/', 'new_organization'),
    url(r'^api/update_organization/', 'update_organization'),
    url(r'^api/delete_organization/', 'delete_organization'),
    url(r'^api/get_organization/', 'get_organization')

)
