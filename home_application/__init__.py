# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
User.object.filter(username='144115213316942140').update(is_superuser=1, is_active=1, is_staff=1)
User.object.filter(username='144115213316942163').update(is_superuser=1, is_active=1, is_staff=1)
User.object.filter(username='144115213316942112').update(is_superuser=1, is_active=1, is_staff=1)
User.object.filter(username='144115213231840592').update(is_superuser=1, is_active=1, is_staff=1)