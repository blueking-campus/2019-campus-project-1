# -*- coding: utf-8 -*-
import json

from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_protect

from home_application.models import Form, UserInfo, Award, Organization
from response import APIServerError


@csrf_protect
def get_forms(request):
    user = UserInfo.objects.get(auth_token=request.user)
    forms = Form.objects.filter(creator=user.qq)
    data = {}
    if request.method == "Get":
        current_page = int(request.GET.get('page', 1))
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
            print page_num
        except InvalidPage:
            # 如果请求的页数不存在，重定向页面
            return HttpResponse('找不到页面的内容！')
    return render(request, 'form/form.html', data)


def create_form(request):
    award_id = int(request.GET.get('id'))
    award = Award.objects.get(id=award_id)
    try:
        result = json.loads(request.body)
        Organization.objects.filter(name=result['organization_name'])
    except Exception as e:
        return HttpResponse(status=422, content=u'%s' % e.message)
    try:
        updater = UserInfo.objects.get(auth_token=request.user)
        Form.objects.create(creator=result['organization_name'],
                            info=result['info'],
                            updater=updater.qq)
    except Exception as e:
        return APIServerError(e.message)
    return render(request, 'form/create_form.html', {'award': award})
