# -*- coding: utf-8 -*-

# import from apps here


# import from lib
# ===============================================================================
from django.contrib import admin
from models import Choice, Permission, Organization

admin.site.register(Choice)
admin.site.register(Permission)
admin.site.register(Organization)
# ===============================================================================
