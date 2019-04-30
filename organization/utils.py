# -*- coding: utf-8 -*-
import re
from home_application.response import APIServerError


def verified_organization(result):
    name = '^[\u4e00-\u9fa5]+$'
    member = '^[1-9][0-9]{4,10}([;|；][1-9][0-9]{4,10})*$'
    if result['name'] != '':
        if re.match(name, result['name']):
            return APIServerError(u"组织名不符合规范")
    else:
        if re.match(member, result['principal']) and re.match(member, result['users']):
            return APIServerError(u"负责人和参评人员需由qq号码组成")