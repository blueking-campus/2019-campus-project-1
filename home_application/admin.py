# -*- coding: utf-8 -*-

# import from apps here


# import from lib
# ===============================================================================
from django.contrib import admin
from models import Choice, Permission, Organization, UserInfo, UserPermission, Award, Form

admin.site.register(Choice)
admin.site.register(Permission)
admin.site.register(Organization)
admin.site.register(UserInfo)
admin.site.register(UserPermission)
admin.site.register(Award)
admin.site.register(Form)
# ===============================================================================
