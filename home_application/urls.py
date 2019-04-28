# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include

urlpatterns = patterns(
    'home_application.views',
    # 首页--your index
    (r'^$', 'home'),
    (r'^dev_guide/$', 'dev_guide'),
    (r'^contact/$', 'contact'),
    (r'^organization/', include('organization.urls')),
)
