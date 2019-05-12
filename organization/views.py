# -*- coding: utf-8 -*-
import json

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from common.mymako import render_mako_context
from home_application.models import Organization, UserInfo
from home_application.response import APIResult, APIServerError
from organization.utils import verified_organization


@csrf_protect
def get_organization_list(request):
    organizations = Organization.objects.all()
    data = {}
    if request.method == "GET":
        current_page = int(request.GET.get('page', 1))
        paginator = Paginator(organizations, 5)
        page_num = paginator.num_pages
        try:
            organization_list = paginator.page(current_page)
            if organization_list.has_next():
                next_page = current_page + 1
            else:
                next_page = current_page
            if organization_list.has_previous():
                previous_page = current_page - 1
            else:
                previous_page = current_page
            data = {
                'count': paginator.count,
                'page_num': range(1, page_num + 1),
                'current_page': current_page,
                'next_page': next_page,
                'previous_page': previous_page,
                'results': organization_list
            }
        except InvalidPage:
            # 如果请求的页数不存在，重定向页面
            return HttpResponse('找不到页面的内容！')
    return render(request, 'organization/organization.html', data)


@csrf_exempt
def new_organization(request):
    try:
        result = json.loads(request.body)
        verified_organization(result)
    except Exception as e:
        return HttpResponse(status=422, content=u'%s' % e.message)
    try:
        updater = UserInfo.objects.get(auth_token=request.user)
        Organization.objects.create(name=result['name'],
                                    principal=result['principal'],
                                    users=result['users'],
                                    updater=updater)
    except:
        return APIServerError(u"创建失败！")
    return render(request, 'organization/organization.html')


@require_POST
def update_organization(request):
    try:
        result = json.loads(request.body)
        organization_id = int(result['id'])
        verified_organization(result)
        organization = Organization.objects.filter(id=organization_id)
        if organization.exists():
            organization.update(name=result['name'])
            organization.update(principal=result['principal'])
            organization.update(users=result['users'])
            organization.update(updater=request.user)
            organization.update(updated_time=result['updated_time'])
    except Exception as e:
        return APIServerError(e.message)
    return render(request, 'organization/organization.html')


def delete_organization(request):
    try:
        result = json.loads(request.body)
        organization_id = int(result['id'])
        organization = Organization.objects.filter(id=organization_id)[0]
        organization.is_delete = True
        organization.save()
    except Exception as e:
        return APIServerError(e.message)
    return render(request, 'organization/organization.html')


def get_organization(request):
    try:
        organization_id = request.GET.get('id')
        organization = Organization.objects.get(id=organization_id)
        data = {
            'id': organization.id,
            'name': organization.name,
            'principal': organization.principal,
            'users': organization.users,
            'updater': organization.updater.qq,
            'updated_time': organization.updated_time
        }
    except Exception as e:
        return APIServerError(e.message)
    return render(request, 'organization/organization_info.html', data)
