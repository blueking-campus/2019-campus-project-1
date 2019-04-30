# -*- coding: utf-8 -*-
from os import path

from django.conf.urls import url, patterns


urlpatterns = patterns(
    'organization.views',
    # url(r'^$', 'home'),
    url(r'^new_organization/', 'new_organization'),
    url(r'^$', 'get_organizations'),
    url(r'^get_organizations/', 'get_organizations'),
    url(r'^update_organization/', 'update_organization'),
    url(r'^delete_organization/$', 'delete_organization'),
    url(r'^get_organization/', 'get_organization')

)
