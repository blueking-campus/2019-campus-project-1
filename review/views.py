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
    返回评审首页
    """
    qq = request.COOKIES.get("uin")
    qq = qq.split('o')[1]
    while True:
        if qq[0] == '0':
            qq = qq[1:]
        else:
            break
    cur_page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 5))
    all_form_counts = Form.objects.filter(creator__contains=qq).count()
    all_page = all_form_counts / limit
    remain = all_form_counts % limit
    if remain > 0:
        all_page += 1
    offset = (cur_page - 1) * limit
    forms = Form.objects.filter(creator__contains=qq)[offset: offset + limit]
    return render(request, "review/review_index.html",
                  {'forms': forms, 'all_page': all_page, 'cur_page': cur_page})


def edit_review(request):
    """
    返回编辑评语页面
    """
    form_id = int(request.GET.get("form_id"))
    form = Form.objects.filter(form_id=form_id).first()
    return render(request, "review/edit_review.html",
                  {'form': form})


def update_review(request):
    """
    更新申请表接口
    """

    if request.method == 'POST':
        try:
            req = json.loads(request.body)
        except:
            response = {
                "result": False,
                "code": 400,
                "data": {},
                "message": "审核失败"
            }
            return APIServerError(response)
        qq = request.COOKIES.get("uin")
        qq = qq.split('o')[1]
        while True:
            if qq[0] == '0':
                qq = qq[1:]
            else:
                break
        form_id = int(req["form_id"])
        comment = req["comment"]
        status = int(req["status"])
        try:
            form = Form.objects.get(form_id=form_id)
        except:
            return APIServerError({
                "result": False,
                "code": 400,
                "data": {},
                "message": "get form id " + form_id + " error"
            })
        form.comment = comment
        form.status = status
        form.updater = qq
        form.save()
        response = {
            "result": True,
            "code": 0,
            "data": {},
            "message": "审核成功"
        }
        return APIResult(response)
    else:
        pass


def reject_form(request):
    """
    驳回指定申请表接口
    """
    form_id = int(request.GET.get('form_id'))
    try:
        Form.objects.get(form_id=form_id).update(status=1)
    except:
        return APIServerError({
            "result": False,
            "code": 400,
            "data": {},
            "message": "get form id "+ form_id +" error"
        })
    return HttpResponseRedirect('/review/')



def pass_form(request):
    """
    通过指定申请表接口
    """
    form_id = int(request.GET.get('form_id'))
    try:
        Form.objects.get(form_id=form_id).update(status=2)
    except:
        return APIServerError({
            "result": False,
            "code": 400,
            "data": {},
            "message": "get form id " + form_id + " error"
        })
    return HttpResponseRedirect('/review/')