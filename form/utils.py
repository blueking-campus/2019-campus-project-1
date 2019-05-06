# -*- coding: utf-8 -*-
import re

from home_application.models import Organization
from home_application.response import APIServerError


def verified_form(result):
    try:
        organization = Organization.objects.filter(name=result['organization_name'])

    except Exception as e:
        return APIServerError(u"该组织不存在！")