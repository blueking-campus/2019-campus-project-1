# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include


urlpatterns = patterns(
    'home_application.views',
    # 首页--your index
    url(r'^$', 'home'),
    # (r'^dev_guide/$', 'dev_guide'),
    # (r'^contact/$', 'contact'),
    url(r'^award/', include('award.urls')),
    url(r'^organization/', include('organization.urls')),
    url(r'^form/', include('form.urls')),
)
