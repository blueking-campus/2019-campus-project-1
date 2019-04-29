# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import json

from django.template import RequestContext

from home_application.models import Award, UserInfo, Choice
from common.mymako import render_mako_context


# Create your views here.

# def index(request):
#     """
#         首页
#     """
#     return render_mako_context(request, '/award/award_index.html')


def create(request):
    """
        新建奖项页面
    """
    return render_mako_context(request, '/award/create_award.html')


def create_award(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        print req
        name = req["name"]
        requirement = req["requirement"]
        organization = req["organization"]
        level = Choice(id=req["level"])
        has_extra_info = req["has_extra_info"]
        status = bool(req["status"])
        print status
        submit_start_time = req["submit_start_time"]
        submit_end_time = req["submit_end_time"]
        try:
            Award.objects.create(name=name, requirement=requirement, organization=organization
                                 , level=level, has_extra_info=has_extra_info, status=status
                                 , submit_start_time=submit_start_time, submit_end_time=submit_end_time)
            response = {
                "result": True,
                "code": 0,
                "data": {},
                "message": "创建奖项成功"
            }
        except:
            response = {
                "result": False,
                "code": 403,
                "data": {},
                "message": "创建奖项失败"
            }
        return HttpResponse(response)
    else:
        return HttpResponse()


def index(request):
    limit = 5
    allAwardCounts = Award.objects.count()
    allPage = allAwardCounts / limit
    remain = allAwardCounts % limit
    if remain > 0:
        allPage += 1
    try:
        curPage = int(request.GET.get('curPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        pageType = ''

    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    offSet = (curPage - 1) * limit
    awards = Award.objects.all()[offSet: offSet + limit]



    return render(request, "award/award_index.html", {'awards': awards, 'allPage': allPage, 'curPage': curPage})