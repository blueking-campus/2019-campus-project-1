# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='organization',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u7ec4\u7ec7', to='home_application.Organization'),
        ),
    ]
