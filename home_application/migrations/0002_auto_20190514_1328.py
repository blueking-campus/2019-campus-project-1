# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='comment',
            field=models.TextField(null=True, verbose_name='\u8bc4\u8bed'),
        ),
        migrations.AlterField(
            model_name='form',
            name='extra_info',
            field=models.FileField(upload_to=b'', null=True, verbose_name='\u9644\u4ef6'),
        ),
        migrations.AlterField(
            model_name='form',
            name='updater',
            field=models.CharField(max_length=20, null=True, verbose_name='\u5ba1\u6279\u8005'),
        ),
    ]
