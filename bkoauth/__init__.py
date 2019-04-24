# -*- coding: utf-8 -*-
try:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass


try:
    get_app_access_token = None
    get_access_token = None
    refresh_token = None
    get_access_token_by_user = None
except:
    pass


def _init_function():
    from . import signals  # noqa
    from .client import oauth_client

    global oauth_client
    global get_app_access_token
    global get_access_token
    global refresh_token
    global get_access_token_by_user

    get_app_access_token = oauth_client.get_app_access_token
    get_access_token = oauth_client.get_access_token
    refresh_token = oauth_client.refresh_token
    get_access_token_by_user = oauth_client.get_access_token_by_user


try:
    from django.apps import AppConfig

    default_app_config = 'bkoauth.BkoauthConfig'

    class BkoauthConfig(AppConfig):
        name = 'bkoauth'

        def ready(self):
            _init_function()
except:
    _init_function()
