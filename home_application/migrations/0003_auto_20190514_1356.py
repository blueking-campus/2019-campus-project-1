# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_auto_20190514_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='comment',
            field=models.TextField(verbose_name='\u8bc4\u8bed', blank=True),
        ),
        migrations.AlterField(
            model_name='form',
            name='updater',
            field=models.CharField(max_length=20, verbose_name='\u5ba1\u6279\u8005', blank=True),
        ),
    ]
