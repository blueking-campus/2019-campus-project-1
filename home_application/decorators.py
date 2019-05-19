# -*- coding: utf-8 -*-
from functools import wraps

from django.shortcuts import render
from django.utils.decorators import available_attrs

from bkoauth.utils import transform_uin
from home_application.utils import is_header, is_principal
from settings import REMOTE_STATIC_URL


def require_admin(func):
    """
    验证是否管理员装饰器
    :return:
    """

    @wraps(func, assigned=available_attrs(func))
    def inner(request, *args, **kwargs):
        uin = request.COOKIES.get('uin', '')
        user_qq = transform_uin(uin)
        if not is_header(request.user, user_qq):
            return render(request, "403.html", {"REMOTE_STATIC_URL": REMOTE_STATIC_URL})
        return func(request, *args, **kwargs)

    return inner


def require_principal(func):
    """
    验证是否负责人
    :return:
    """

    @wraps(func, assigned=available_attrs(func))
    def inner(request, *args, **kwargs):
        uin = request.COOKIES.get('uin', '')
        user_qq = transform_uin(uin)
        if not is_principal(request.user, user_qq):
            return render(request, "403.html", {"REMOTE_STATIC_URL": REMOTE_STATIC_URL})
        return func(request, *args, **kwargs)

    return inner
