# -*- coding: utf-8 -*-
from django.shortcuts import render

from common.mymako import render_mako_context


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt【装饰器引入from account.decorators import login_exempt】
from home_application.models import Award


def home(request):
    awards_list = Award.objects.filter(status=True).order_by('-id')[:3]
    awards = Award.to_array(awards_list)
    # print awards
    return render(request, 'home_application/home.html', {'results': awards})


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contact(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')
