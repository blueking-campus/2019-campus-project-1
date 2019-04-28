# -*- coding: utf-8 -*-
import json
import re

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.views.generic.base import View

from common.mymako import render_mako_context, render_json
from home_application.models import Organization
from home_application.response import APIResult
from organization.utils import verified_organization


@csrf_protect
def organization_home(request):
    # data = {}
    # if show_organizations.code == 0:
    data = show_organizations.data
    return render_mako_context(request, 'organization/organization.html', {'data': data})


@csrf_protect
@require_GET
def show_organizations(request):
    organizations = Organization.objects.all()
    paginator = Paginator(organizations, 5)
    data = {}
    if request.method == "GET":
        current_page = int(request.GET.get('page', 1))
        try:
            organization_list = paginator.page(current_page)
        except PageNotAnInteger:
            # 如果请求的不是整数，返回第一页
            organization_list = paginator.page(1)
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页
            organization_list = paginator.page(paginator.num_pages)
        except InvalidPage:
            # 如果请求的页数不存在，重定向页面
            return HttpResponse('找不到页面的内容！')
        data = {
            'count': paginator.count,
            'results': Organization.to_array(organization_list)
        }
    # return APIResult(0, data, "返回所有组织成功！")
    return render_mako_context(request, 'organization/organization.html', {'data': data})


@require_POST
@csrf_exempt
def new_organization(request):
    try:
        result = json.loads(request.body)
        verified_organization(result)
    except Exception as e:
        return HttpResponse(status=422, content=u'%s' % e.message)
    try:
        Organization.objects.create(name=result['name'],
                                    principal=result['principal'],
                                    users=result['users'],
                                    updater=request.user)
    except Exception as e:
        return APIResult(400, message=e.message)
    return APIResult(0, u"创建组织成功！")


@require_POST
def update_organization(request, organization_id):
    try:
        result = json.dumps(request.body)
        verified_organization(result)
    except Exception as e:
        return HttpResponse(status=422, content=u'%s' % e.message)
    try:
        organization = Organization.objects.filter(id=organization_id)
        organization.name = result['name']
        organization.principal = result['principal']
        organization.users = result['users']
        organization.updater = request.user
        organization.save()
    except Exception as e:
        return APIResult(400, message=e.message)


def del_organization(request, organization_id):
    try:
        Organization.objects.filter(id=organization_id).delete()
    except Exception as e:
        return APIResult(410, message=e.message)
    return APIResult(204, "删除成功！")


# def get_organization(request, organization_id):
#     try:
#         organization = Organization.objects.get(id=organization_id)
#     except Exception as e:
#         return APIResult(404, e.message)
#     return APIResult()