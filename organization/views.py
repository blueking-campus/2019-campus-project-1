# -*- coding: utf-8 -*-
import json

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from common.mymako import render_mako_context
from home_application.models import Organization
from home_application.response import APIResult, APIServerError
from organization.utils import verified_organization


def home(request):
    count = 5
    real_page = Organization.objects.all().count()/5+1
    if real_page < 5:
        count = real_page
    return render(request, 'organization/organization.html', {'count': range(1, count+1)})


@csrf_protect
def get_organizations(request):
    organizations = Organization.objects.all()
    data = {}
    if request.method == "GET":
        current_page = request.GET.get('page', 1)
        # current_page = 1
        paginator = Paginator(organizations, 5)
        page_num = paginator.num_pages
        try:
            organization_list = paginator.page(current_page)
            if organization_list.has_next():
                next_page = current_page+1
            else:
                next_page = current_page
            if organization_list.has_previous():
                previous_page = current_page-1
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
    # data = {}
    # if request.method == "GET":
    #     page = int(request.GET.get('page'), 1)
    #     limit = 5
    #     offset = (page - 1) * limit
    #     query_set = organizations[offset:limit+offset]
    #     count = query_set[offset:limit+offset].count()
    #     data = {
    #         'count': count,
    #         'curr_page': page,
    #
    #         'results': Organization.to_array(query_set)
    #     }
    # return render(request, 'organization/organization.html', data)


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
        return APIServerError(e.message)
    return render(request, 'organization/organization.html')


@require_POST
def update_organization(request):
    result = json.loads(request.body)
    organization_id = int(result['id'])
    verified_organization(result)
    try:
        organization = Organization.objects.filter(id=organization_id)
        if organization.exists():
            organization.update(name=result['name'])
            organization.update(principal=result['principal'])
            organization.update(users=result['users'])
            organization.update(updater=request.user)
    except Exception as e:
        return APIServerError(e.message)
    return render(request, 'organization/organization.html')


def delete_organization(request):
    organization_id = int(request.GET.get('id'))
    try:
        organization = Organization.objects.filter(id=organization_id)
        organization.delete()
    except Exception as e:
        return APIServerError(e.message)
    return render(request, 'organization/organization.html')


def get_organization(request):
    try:
        organization_id = request.GET.get('id')
        organization = Organization.objects.get(id=organization_id)
        # data = {
        #     'name': organization.name,
        #     'principal': organization.principal,
        #     'users': organization.users
        # }
    except Exception as e:
        return APIServerError(e.message)
    return render(request, 'organization/organization.html', {'organization': organization})
