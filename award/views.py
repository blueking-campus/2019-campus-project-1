# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from response import APIResult, APIServerError
from home_application.models import Award, UserInfo, Organization, Form, Choice
import json


# Create your views here.

def index(request):
    try:
        cur_page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 5))
    except ValueError:
        cur_page = 1
        limit = 5
    allAwardCounts = Award.objects.filter(is_delete=False).count()
    allPage = allAwardCounts / limit
    remain = allAwardCounts % limit
    if remain > 0:
        allPage += 1
    offset = (cur_page - 1) * limit
    awards = Award.objects.filter(is_delete=0)[offset: offset + limit]

    return render(request, "award/award_index.html", {'awards': awards, 'allPage': allPage, 'cur_page': cur_page})


def create(request):
    """
        新建奖项页面
    """
    levels = Choice.objects.all()
    return render(request, 'award/create_award.html', {'levels': levels})


def create_award(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        name = req["name"]
        requirement = req["requirement"]
        organization = req["organization"]
        level = Choice(id=req["level"])
        has_extra_info = req["has_extra_info"]
        status = bool(req["status"])
        submit_start_time = req["submit_start_time"]
        submit_end_time = req["submit_end_time"]
        response = {
            "result": True,
            "code": 0,
            "data": {},
            "message": "创建奖项成功"
        }
        Award.objects.create(name=name, requirement=requirement, organization=organization
                             , level=level, has_extra_info=has_extra_info, status=status
                             , submit_start_time=submit_start_time, submit_end_time=submit_end_time)

        return APIResult(response)
    else:
        pass


def get_award(request):
    try:
        award_id = int(request.GET.get('award_id'))
        cur_page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 5))
    except ValueError:
        award_id = 1
        cur_page = 1
        limit = 5
    award = Award.objects.get(id=award_id)
    all_form_counts = Form.objects.filter(award_id=award.id).count()
    allPage = all_form_counts / limit
    remain = all_form_counts % limit
    if remain > 0:
        allPage += 1
    offset = (cur_page - 1) * limit
    organization = Organization.objects.get(name=award.organization)
    principal = organization.principal
    forms = Form.objects.filter(award_id=award.id)[offset: offset + limit]
    return render(request, "award/award_info.html",
                  {'award': award, 'principal': principal, 'forms': forms, 'allPage': allPage, 'cur_page': cur_page})


def delete_award(request):
    try:
        award_id = int(request.GET.get('award_id'))
    except ValueError:
        award_id = 1

    award = Award.objects.get(id=award_id)
    award.is_delete = True
    award.save()
    return HttpResponseRedirect('/award/')


def edit_award(request):
    try:
        award_id = int(request.GET.get('award_id'))
    except ValueError:
        award_id = 1

    award = Award.objects.get(id=award_id)
    levels = Choice.objects.all()
    return render(request, "award/edit_award.html", {'award': award, 'levels': levels})


def update_award(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        id = int(req["id"])
        name = req["name"]
        requirement = req["requirement"]
        organization = req["organization"]
        level = Choice(id=req["level"])
        has_extra_info = req["has_extra_info"]
        status = bool(req["status"])
        submit_start_time = req["submit_start_time"]
        submit_end_time = req["submit_end_time"]
        response = {
            "result": True,
            "code": 0,
            "data": {},
            "message": "修改奖项成功"
        }
        award = Award.objects.get(id=id)
        award.name = name
        award.requirement = requirement
        award.organization = organization
        award.level = level
        award.has_extra_info = has_extra_info
        award.status = status
        award.submit_start_time = submit_start_time
        award.submit_end_time = submit_end_time
        award.save()
        return APIResult(response)
    else:
        pass
