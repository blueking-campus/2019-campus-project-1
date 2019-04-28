# -*- coding: utf-8 -*-
import re


def verified_organization(result):
    if result['name'] != '':
        if re.match(r'^[\u4e00-\u9fa5]+$', result['name']) is None:
            raise Exception(u'组织名含有非法字符')
    else:
        if re.match(r'^[0-9;]+$', result['principal']) & re.match(r'^[0-9;]+$', result['users']) is None:
            raise Exception(u'负责人和参评人员需由qq号码组成')