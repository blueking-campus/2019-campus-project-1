# -*- coding: utf-8 -*-
import json
import datetime

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from response import APIResult, APIServerError
from home_application.models import Award, Organization, Form, Choice


# Create your views here.

def index(request):
    """
    返回奖项首页
    """
    cur_page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 5))
    all_award_counts = Award.objects.filter(is_delete=False).count()
    all_page = all_award_counts / limit
    remain = all_award_counts % limit
    if remain > 0:
        all_page += 1
    offset = (cur_page - 1) * limit
    awards = Award.objects.filter(is_delete=0)[offset: offset + limit]
    organizations = Organization.objects.all()
    return render(request, "award/award_index.html",
                  {'awards': Award.to_array(awards), 'all_page': all_page, 'cur_page': cur_page, 'organizations': organizations})


def create(request):
    """
    返回创建奖项页面
    """
    levels = Choice.objects.all()
    organizations = Organization.objects.all()
    return render(request, 'award/create_award.html', {'levels': levels, 'organizations': organizations})


def clone_award(request):
    """
    返回克隆奖项页面
    """
    organizations = Organization.objects.all()
    return render(request, 'award/clone_award.html', {'organizations': organizations})


def create_award(request):
    """
    创建奖项接口
    """
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
        except:
            response = {
                "result": False,
                "code": 400,
                "data": {},
                "message": "创建奖项失败"
            }
            return APIServerError(response)
        name = req["name"]
        requirement = req["requirement"]
        organization = Organization(id=int(req["organization"]))
        level = Choice(id=int(req["level"]))
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
        Award.objects.create(
            name=name, requirement=requirement, organization=organization
            , level=level, has_extra_info=has_extra_info, status=status
            , submit_start_time=submit_start_time, submit_end_time=submit_end_time)

        return APIResult(response)
    else:
        pass


def get_award(request):
    """
    获取指定奖项信息接口
    """
    award_id = int(request.GET.get('award_id'))
    cur_page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 5))
    try:
        award = Award.objects.get(id=award_id)
    except:
        return APIServerError({
            "result": False,
            "code": 500,
            "data": {},
            "message": "get award id error"
        })
    all_form_counts = Form.objects.filter(award_id=award.id).count()
    all_page = all_form_counts / limit
    remain = all_form_counts % limit
    if remain > 0:
        all_page += 1
    offset = (cur_page - 1) * limit
    organization = Organization.objects.get(id=award.organization.id)
    principal = organization.principal
    forms = Form.objects.filter(award_id=award.id)[offset: offset + limit]
    return render(request, "award/award_info.html", {'award': award, 'principal': principal,
                                                     'forms': forms, 'all_page': all_page, 'cur_page': cur_page})


def delete_award(request):
    """
    软删除指定奖项信息接口
    """
    award_id = int(request.GET.get('award_id'))
    try:
        award = Award.objects.get(id=award_id)
    except:
        return APIServerError({
            "result": False,
            "code": 400,
            "data": {},
            "message": "get award id error"
        })
    award.is_delete = True
    award.save()
    return HttpResponseRedirect('/award/')


def edit_award(request):
    """
    返回编辑奖项页面
    """
    award_id = int(request.GET.get('award_id'))
    try:
        award = Award.objects.get(id=award_id)
    except:
        return APIServerError({
            "result": False,
            "code": 400,
            "data": {},
            "message": "get award id error"
        })
    levels = Choice.objects.all()
    return render(request, "award/edit_award.html", {'award': award, 'levels': levels})


def update_award(request):
    """
    更新指定奖项信息接口
    """
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
        except:
            response = {
                "result": False,
                "code": 400,
                "data": {},
                "message": "编辑奖项失败"
            }
            return APIServerError(response)
        id = int(req["id"])
        name = req["name"]
        requirement = req["requirement"]
        organization = Organization.objects.get(name=req["organization"])
        level = Choice(id=req["level"])
        has_extra_info = req["has_extra_info"]
        status = bool(req["status"])
        submit_start_time = req["submit_start_time"]
        submit_end_time = req["submit_end_time"]

        try:
            award = Award.objects.get(id=id)
        except:
            return APIServerError({
                "result": False,
                "code": 400,
                "data": {},
                "message": "get award id error"
            })
        award.name = name
        award.requirement = requirement
        award.organization = organization
        award.level = level
        award.has_extra_info = has_extra_info
        award.status = status
        award.submit_start_time = submit_start_time
        award.submit_end_time = submit_end_time
        award.save()
        response = {
            "result": True,
            "code": 0,
            "data": {},
            "message": "修改奖项成功"
        }
        return APIResult(response)
    else:
        pass


def search_award(request):
    """
    搜索指定奖项信息接口
    """
    UNLIMITED_CODE = -1
    name = request.GET.get("name")
    organization_id = int(request.GET.get("organization_id"))
    time = request.GET.get("time")
    status = int(request.GET.get("status"))
    limit = 5
    offset = 0
    start_time = time.split(u"&nbsp;-&nbsp;")[0].split(u'/')
    end_time = time.split(u"&nbsp;-&nbsp;")[1].split(u'/')
    start_time = datetime.datetime(int(start_time[0]), int(start_time[1]), int(start_time[2]))
    end_time = datetime.datetime(int(end_time[0]), int(end_time[1]), int(end_time[2]))
    if status == UNLIMITED_CODE:
        awards = Award.objects.filter(
            name__contains=name,
            submit_start_time__range=(start_time, end_time),
            submit_end_time__range=(start_time, end_time),
            organization_id=organization_id
        )
    else:
        awards = Award.objects.filter(
            name__contains=name,
            submit_start_time__range=(start_time, end_time),
            submit_end_time__range=(start_time, end_time),
            organization_id=organization_id,
            status=status
        )
    count = awards.count()
    cur_page = 1
    all_page = count / limit
    remain = count % limit
    if remain > 0:
        all_page += 1
    awards = awards[offset: offset + limit]
    organizations = Organization.objects.all()
    return render(request, "award/award_index.html",
                  {'awards': awards, 'all_page': all_page, 'cur_page': cur_page, 'organizations': organizations})


def clone_preview(request):
    """
    返回批量克隆预览结果
    """
    if request.method == "POST":
        try:
            req = json.loads(request.body)
        except:
            response = {
                "result": False,
                "code": 400,
                "data": {},
                "message": "克隆奖项失败"
            }
            return APIServerError(response)
        pre_name = req["pre_name"]
        name = req["name"]
        organization_ids = req["organization_ids"]
        time = req["time"]
        limit = req["limit"]
        offset = req["offset"]
        start_time = time.split(u" - ")[0].split(u'/')
        end_time = time.split(u" - ")[1].split(u'/')
        start_time = datetime.datetime(int(start_time[0]), int(start_time[1]), int(start_time[2]))
        end_time = datetime.datetime(int(end_time[0]), int(end_time[1]), int(end_time[2]))
        awards = Award.objects.filter(
            name__contains=pre_name,
            submit_start_time__range=(start_time, end_time),
            submit_end_time__range=(start_time, end_time),
            organization_id__in=organization_ids
        )
        count = awards.count()
        all_pages = count / limit
        awards = awards[offset: offset + limit]
        session = {}
        session['all_pages'] = all_pages
        session['count'] = count
        session['result'] = [
            {
                "id": award.id,
                "pre_name": award.name,
                "name": award.name.replace(pre_name, name),
                "organization": award.organization.name,
                "level": award.level.name,
                "submit_start_time": award.submit_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                "submit_end_time": award.submit_end_time.strftime('%Y-%m-%d %H:%M:%S')
            } for award in awards
        ]
        return JsonResponse(json.dumps(session), safe=False)
    else:
        pass


def clone_award_info(request):
    """
    返回指定克隆奖项信息页面
    """
    award_id = int(request.GET.get('award_id'))
    cur_page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 5))
    try:
        award = Award.objects.get(id=award_id)
    except:
        return APIServerError({
            "result": False,
            "code": 400,
            "data": {},
            "message": "get award id error"
        })
    all_form_counts = Form.objects.filter(award_id=award.id).count()
    allPage = all_form_counts / limit
    remain = all_form_counts % limit
    if remain > 0:
        allPage += 1
    offset = (cur_page - 1) * limit
    organization = Organization.objects.get(id=award.organization.id)
    principal = organization.principal
    forms = Form.objects.filter(award_id=award.id)[offset: offset + limit]
    return render(request, "award/clone_award_info.html", {'award': award, 'principal': principal,
                                                           'forms': forms, 'allPage': allPage, 'cur_page': cur_page})


def edit_clone_award(request):
    """
    返回编辑指定克隆奖项信息页面
    """
    award_id = int(request.GET.get('award_id'))
    try:
        award = Award.objects.get(id=award_id)
    except:
        return APIServerError({
            "result": False,
            "code": 400,
            "data": {},
            "message": "get award id error"
        })
    levels = Choice.objects.all()
    return render(request, "award/edit_clone_award.html", {'award': award, 'levels': levels})


def save_clone_award(request):
    """
    保存批量克隆结果接口
    """
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
        except:
            response = {
                "result": False,
                "code": 400,
                "data": {},
                "message": "保存奖项失败"
            }
            return APIServerError(response)
        if req == []:
            response = {
                "result": True,
                "code": 0,
                "data": {},
                "message": "请先选择要批量克隆的选项"
            }
            return APIResult((response))
        for award in req:
            id = award["id"]
            name = award["name"]
            try:
                requirement = award["requirement"]
                has_extra_info = award["has_extra_info"]
                status = bool(award["status"])
            except KeyError:
                requirement = Award.objects.get(id=id).requirement
                has_extra_info = Award.objects.get(id=id).has_extra_info
                status = Award.objects.get(id=id).status
            org_id = Organization.objects.get(name=award["organization"]).id
            level_id = Choice.objects.get(name=award["level"]).id
            organization = Organization(id=org_id)
            level = Choice(id=level_id)
            submit_start_time = datetime.datetime.strptime(award["submit_start_time"], "%Y-%m-%d %H:%M:%S")
            submit_end_time = datetime.datetime.strptime(award["submit_end_time"], "%Y-%m-%d %H:%M:%S")
            Award.objects.create(
                name=name, requirement=requirement, organization=organization
                , level=level, has_extra_info=has_extra_info, status=status
                , submit_start_time=submit_start_time, submit_end_time=submit_end_time)
        response = {
            "result": True,
            "code": 0,
            "data": {},
            "message": "创建奖项成功"
        }
        return APIResult(response)
