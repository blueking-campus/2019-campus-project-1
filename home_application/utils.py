# -*- coding: utf-8 -*-
from models import UserPermission, Organization


def is_header(self, user_qq):
    """
    是否负责人
    """
    if self.is_superuser:
        return True
    return UserPermission.objects.filter(qq=user_qq, permission=1).exists()


def is_principal(self, user_qq):
    """
    是否该组织head
    :param user_qq:
    :return:
    """
    if self.is_superuser:
        return True
    return UserPermission.objects.filter(qq=user_qq, permission=1).exists() or Organization.objects.filter(
        principal__contains=qq).exists()
