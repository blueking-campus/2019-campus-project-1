# -*- coding: utf-8 -*-
import json
import os
import datetime

from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from home_application.models import Form, UserInfo, Award, Organization
from home_application.response import APIResult
from response import APIServerError


# 获取当前登录用户所申报的所有内容
@csrf_protect
def get_form_list(request):
    user = UserInfo.objects.filter(auth_token=request.user).first()
    all_award = Award.objects.filter(status=True)
    all_award = Award.my_award(all_award, user.qq)
    data = {}
    if request.method == "GET":
        current_page = int(request.GET.get('page', 1))
        paginator = Paginator(all_award, 5)
        page_num = paginator.num_pages
        try:
            award_list = paginator.page(current_page)
            if award_list.has_next():
                next_page = current_page + 1
            else:
                next_page = current_page
            if award_list.has_previous():
                previous_page = current_page - 1
            else:
                previous_page = current_page
            data = {
                'count': paginator.count,
                'page_num': range(1, page_num + 1),
                'current_page': current_page,
                'next_page': next_page,
                'previous_page': previous_page,
                'results': award_list
            }
        except InvalidPage:
            # 如果请求的页数不存在，重定向页面
            return HttpResponse('找不到页面的内容！')
    return render(request, 'form/form.html', data)


# 新建申报
def create_form(request, award_id):
    CHOICE_STATUS = 0
    award = Award.objects.get(id=award_id)
    organization = Organization.objects.get(name=award.organization.name)
    principal = organization.principal
    if request.method == "POST":
        extra_info = request.FILES.get('appendix')
        applicant = request.POST.get("applicant")
        info = request.POST.get("info")
        updater = UserInfo.objects.filter(auth_token=request.user)[0]
        if extra_info is None:
            Form.objects.create(creator=applicant,
                                info=info,
                                award=award,
                                updater=updater.qq,
                                status=CHOICE_STATUS)
        else:
            file_name = 'static/file/%s' % extra_info.name
            with open(file_name, 'wb+') as destination:
                for chunk in extra_info.chunks():
                    destination.write(chunk)
            Form.objects.create(creator=applicant,
                                info=info,
                                award=award,
                                updater=updater.qq,
                                extra_info=extra_info,
                                status=CHOICE_STATUS)
        response = {
            "result": True,
            "code": 0,
            "data": {},
            "message": "创建申报书成功"
        }
        return APIResult(response)
    else:
        IS_NEED_AFFIX = 0
        if award.has_extra_info:
            IS_NEED_AFFIX = 1
        return render(request, 'form/create_form.html', {'award': award,
                                                         'principal': principal,
                                                         'affix': IS_NEED_AFFIX})


def get_form(request, award_id):
    award = Award.objects.get(id=award_id)
    try:
        organization = Organization.objects.get(name=award.organization.name)
    except:
        response = {
            "result": False,
            "code": 400,
            "data": {},
            "message": "该组织不存在"
        }
        return APIResult(response)
    principal = organization.principal
    form_id = request.GET.get('id')
    form = Form.objects.get(form_id=form_id)
    file_name = form.extra_info.name
    data = {
        'award': award,
        'principal': principal,
        'form': form,
        'file_name': file_name
    }
    return render(request, 'form/form_info.html', data)


def update_form(request, form_id):
    applicant = request.POST.get("applicant")
    info = request.POST.get("info")
    extra_info = request.FILES.get('appendix')
    form = Form.objects.filter(form_id=form_id)
    if extra_info is None:
        form.update(creator=applicant, info=info)
    else:
        file_name = 'static/file/%s' % extra_info.name
        with open(file_name, 'wb+') as destination:
            for chunk in extra_info.chunks():
                destination.write(chunk)
        form.update(creator=applicant, info=info, extra_info=extra_info)
    response = {
        "result": True,
        "code": 0,
        "data": {},
        "message": "修改申报书成功"
    }
    return APIResult(response)


def search_form(request):
    CHOICE_STATUS = -1
    name = request.GET.get('name')
    time = request.GET.get('time')
    status = int(request.GET.get('status'))
    current_page = int(request.GET.get('page', 1))
    start_time = time.split(u"&nbsp;-&nbsp;")[0].split(u'/')
    end_time = time.split(u"&nbsp;-&nbsp;")[1].split(u'/')
    start_time = datetime.datetime(int(start_time[0]), int(start_time[1]), int(start_time[2]))
    end_time = datetime.datetime(int(end_time[0]), int(end_time[1]), int(end_time[2]))
    if status == CHOICE_STATUS:
        forms = Form.objects.filter(
            award__name__contains=name,
            updated_time__range=(start_time, end_time)
        )
    else:
        forms = Form.objects.filter(
            award__name__contains=name,
            updated_time__range=(start_time, end_time),
            status=status
        )
    paginator = Paginator(forms, 5)
    page_num = paginator.num_pages
    try:
        form_list = paginator.page(current_page)
        if form_list.has_next():
            next_page = current_page + 1
        else:
            next_page = current_page
        if form_list.has_previous():
            previous_page = current_page - 1
        else:
            previous_page = current_page
        data = {
            'count': paginator.count,
            'page_num': range(1, page_num + 1),
            'current_page': current_page,
            'next_page': next_page,
            'previous_page': previous_page,
            'results': form_list
        }
    except InvalidPage:
        # 如果请求的页数不存在，重定向页面
        return HttpResponse('找不到页面的内容！')
    return render(request, 'form/form.html', data)
