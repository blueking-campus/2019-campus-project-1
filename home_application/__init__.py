# coding=utf-8
from account.models import BkUser

BkUser.objects.filter(username='144115213316942140').update(is_superuser=1, is_active=1, is_staff=1)
BkUser.objects.filter(username='144115213316942163').update(is_superuser=1, is_active=1, is_staff=1)
BkUser.objects.filter(username='144115213316942112').update(is_superuser=1, is_active=1, is_staff=1)
BkUser.objects.filter(username='144115213231840592').update(is_superuser=1, is_active=1, is_staff=1)
