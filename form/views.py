# -*- coding: utf-8 -*-
import json
import os

from django import forms
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from home_application.models import Form, UserInfo, Award, Organization
from home_application.response import APIResult
from response import APIServerError


# 获取当前登录用户所申报的所有内容
@csrf_protect
def get_forms(request):
    user = UserInfo.objects.filter(auth_token=request.user)[0]
    all_form = Form.objects.filter(updater=user.qq).all()
    data = {}
    if request.method == "GET":
        current_page = int(request.GET.get('page', 1))
        paginator = Paginator(all_form, 5)
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


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


def handle_uploaded_file(f):
    with open('static/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# 新建申报
def create_form(request, award_id):
    award = Award.objects.get(id=award_id)
    organization = Organization.objects.get(name=award.organization)
    principal = organization.principal
    if request.method == "POST":
        # 文件上传还未实现
        # extra_info = UploadFileForm(request.POST, request.FILES)
        # if extra_info.is_valid():
            # handle_uploaded_file(extra_info)
        result = {}
        try:
            result = json.loads(request.body)
        except Exception as e:
            return HttpResponse(status=422, content=u'%s' % e.message)
        Organization.objects.filter(name=result['organization_name'])
        try:
            updater = UserInfo.objects.get(auth_token=request.user)
            Form.objects.create(creator=result['organization_name'],
                                info=result['info'],
                                award=award,
                                updater=updater.qq,
                                # extra_info=request.FILES['extra_info'],
                                status=0)
        except:
            return APIServerError(u"创建失败！")
    return render(request, 'form/create_form.html', {'award': award,
                                                     'principal': principal})
